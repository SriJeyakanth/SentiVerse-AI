

# Import necessary libraries
import pandas as pd
import io
import sqlite3
from transformers import pipeline
import ipywidgets as widgets
from IPython.display import display

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('feedback_history.db')
cursor = conn.cursor()

# Create a table to store feedback history if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS FeedbackHistory (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FileName TEXT,
    Text TEXT,
    Sentiment TEXT
)
''')
conn.commit()

# Create buttons for options
analyze_csv_button = widgets.Button(
    description="ANALYZE CSV",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)

view_history_button = widgets.Button(
    description="VIEW HISTORY",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)

# Output area to display widgets dynamically
output = widgets.Output()

# Function to handle CSV analysis
def on_analyze_csv_click(b):
    with output:
        output.clear_output()

        # CSV upload widget
        upload = widgets.FileUpload(
            accept='.csv',
            description="IMPORT CSV",
            layout=widgets.Layout(width='100%', height='50px', margin='10px 0')
        )

        def on_file_upload(change):
            with output:
                output.clear_output()

                uploaded_file = next(iter(upload.value.values()))
                content = uploaded_file['content']
                file_name = uploaded_file.get('name', 'Unknown File')  # Handle missing file name
                df = pd.read_csv(io.StringIO(content.decode('utf-8')))

                # Check if 'Text' column exists; otherwise use the first column
                text_column = 'Text' if 'Text' in df.columns else df.columns[0]
                sentiments = df[text_column].apply(lambda text: sentiment_analyzer(text)[0]['label'])

                # Insert the analyzed data into the database
                for _, row in df.iterrows():
                    cursor.execute('''
                        INSERT INTO FeedbackHistory (FileName, Text, Sentiment)
                        VALUES (?, ?, ?)
                    ''', (file_name, row[text_column], sentiments.loc[_]))
                conn.commit()

                # Calculate overall sentiment score
                sentiment_counts = sentiments.value_counts()
                total_entries = len(df)
                positive_count = sentiment_counts.get('POSITIVE', 0)
                negative_count = sentiment_counts.get('NEGATIVE', 0)
                neutral_count = sentiment_counts.get('NEUTRAL', 0)

                # Calculate score as the percentage of positive entries
                if total_entries > 0:
                    overall_score = (positive_count / total_entries) * 100
                else:
                    overall_score = 0

                # Display the analyzed data as a tabular column and show overall score
                print(f"\nOverall Sentiment Score: {overall_score:.2f}%")
                display(df)

                print("\nCSV data has been analyzed and stored successfully.")

        upload.observe(on_file_upload, names='value')
        display(upload)

# Function to view history
def on_view_history_click(b):
    with output:
        output.clear_output()

        # Fetch all feedback history from the database
        history_df = pd.read_sql_query('SELECT * FROM FeedbackHistory', conn)

        # Calculate overall sentiment score
        sentiment_counts = history_df['Sentiment'].value_counts()
        total_entries = len(history_df)
        positive_count = sentiment_counts.get('POSITIVE', 0)
        negative_count = sentiment_counts.get('NEGATIVE', 0)
        neutral_count = sentiment_counts.get('NEUTRAL', 0)

        # Calculate score as the percentage of positive entries
        if total_entries > 0:
            overall_score = (positive_count / total_entries) * 100
        else:
            overall_score = 0

        # Display history as a full-screen table and show overall score
        print(f"\nOverall Sentiment Score: {overall_score:.2f}%")
        
        # Use pandas' built-in styling to display it in full width
        history_df.style.set_properties(**{'width': '100%', 'max-width': '100%'})
        display(history_df)

# Link buttons to functions
analyze_csv_button.on_click(on_analyze_csv_click)
view_history_button.on_click(on_view_history_click)

# Display the interface
display(analyze_csv_button, view_history_button, output)
