# Import necessary libraries
import pandas as pd
import random
import io
from transformers import pipeline
import ipywidgets as widgets
from IPython.display import display

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# Load additional sentiment datasets and combine them
try:
    positive_df = pd.read_csv('positive.csv')
    negative_df = pd.read_csv('negative.csv')
    tamil_bw_df = pd.read_csv('tamilbw.csv')
except FileNotFoundError as e:
    print(f"Error: {e}\nEnsure all the required files are in the same directory as the script.")

# Combine additional datasets into a single dictionary for lookup
custom_sentiment_dict = {
    word.lower(): 'POSITIVE' for word in positive_df.iloc[:, 0]
}
custom_sentiment_dict.update({
    word.lower(): 'NEGATIVE' for word in negative_df.iloc[:, 0]
})
custom_sentiment_dict.update({
    word.lower(): 'NEGATIVE' for word in tamil_bw_df.iloc[:, 0]
})

# Add Tamil sentiment mappings
sentiment_mapping = {
    'nallathu': 'POSITIVE',
    'nallavan': 'POSITIVE',
    'sandhosam': 'POSITIVE',
    'aanandham': 'POSITIVE',
    'super': 'POSITIVE',
    'semma': 'POSITIVE',
    'chanceless': 'POSITIVE',
    'magilchi': 'POSITIVE',
    'kettathu': 'NEGATIVE',
    'mosam': 'NEGATIVE',
    'drogram': 'NEGATIVE',
    'kobam': 'NEGATIVE',
    'erichal': 'NEGATIVE',
    'aathiram': 'NEGATIVE',
    'koothi': 'NEGATIVE',
    'sunni': 'NEGATIVE',
    'punda': 'NEGATIVE',
    'pundamavane': 'NEGATIVE',
    'othalaka': 'NEGATIVE',
    'roudhiram': 'NEGATIVE',
    'paravala': 'NEUTRAL',
    'anyway good': 'NEUTRAL',
    'not bad': 'NEUTRAL',
    'need improvement': 'NEUTRAL',
    'needs improvement': 'NEUTRAL',
}
custom_sentiment_dict.update(sentiment_mapping)

# Global list to store history
history = []

# Create buttons for the initial options
analyze_text_button = widgets.Button(
    description="ANALYZE TEXT",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)
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

# Custom function to analyze sentiment using additional datasets
def custom_sentiment_analysis(text):
    words = text.split()
    positive_count = sum(1 for word in words if word in custom_sentiment_dict and custom_sentiment_dict[word] == 'POSITIVE')
    negative_count = sum(1 for word in words if word in custom_sentiment_dict and custom_sentiment_dict[word] == 'NEGATIVE')

    if positive_count > negative_count:
        return 'POSITIVE'
    elif negative_count > positive_count:
        return 'NEGATIVE'
    else:
        return None  # Neutral or no custom match

# Function to generate a dynamic response based on sentiment
def generate_dynamic_response(sentiment, score):
    responses = {
        'POSITIVE': [
            "You're on top of the world! Keep spreading the positivity! 😊",
            "What a wonderful mood! You're glowing with happiness! ✨",
            "Keep shining, you're making the world brighter! 💛"
        ],
        'NEGATIVE': [
            "Don't let the storm clouds rain on your day. You got this! 🌈",
            "Mind your words, positivity will brighten your world 💬",
            "Don't let negativity consume you, you're stronger than this! 🌟"
        ],
        'NEUTRAL': [
            "Things are steady, nothing to worry about. Just keep going. 😊",
            "It’s a neutral day, take it easy and stay balanced. ✨",
            "No strong emotions today, but you’re doing just fine. 🌿"
        ]
    }
    return random.choice(responses.get(sentiment, ["Stay positive and keep going!"]))

# Function to display the result
def display_sentiment(sentiment, score, response):
    print(f"SENTIMENT: {sentiment}\n\nSCORE: {score:.2f}/100\n\n{response}")

# Function to handle text analysis
def on_analyze_text_click(b):
    with output:
        output.clear_output()
        text_input = widgets.Textarea(value='', placeholder='Type your text here...', layout=widgets.Layout(width='100%', height='100px', margin='10px 0'))
        analyze_button = widgets.Button(description="Analyze Sentiment", layout=widgets.Layout(width='100%', height='50px', margin='10px 0'))

        def on_button_click(b):
            with output:
                output.clear_output()
                text = text_input.value.lower()
                custom_sentiment = custom_sentiment_analysis(text)
                if custom_sentiment:
                    sentiment = custom_sentiment
                    score = 100 if sentiment == 'POSITIVE' else 0
                else:
                    result = sentiment_analyzer(text)
                    sentiment = result[0]['label']
                    score = result[0]['score'] * 100
                response = generate_dynamic_response(sentiment, score)
                history.append({"Input": text, "Sentiment": sentiment, "Score": score, "Type": "Text"})
                display_sentiment(sentiment, score, response)

        analyze_button.on_click(on_button_click)
        display(text_input, analyze_button)

# Function to handle CSV analysis
def on_analyze_csv_click(b):
    with output:
        output.clear_output()
        upload = widgets.FileUpload(accept='.csv', description="IMPORT CSV", layout=widgets.Layout(width='100%', height='50px', margin='10px 0'))

        def on_file_upload(change):
            with output:
                output.clear_output()
                uploaded_file = next(iter(upload.value.values()))
                content = uploaded_file['content']
                df = pd.read_csv(io.StringIO(content.decode('utf-8')))
                text_column = 'Text' if 'Text' in df.columns else df.columns[0]
                df['Sentiment'] = df[text_column].apply(lambda text: custom_sentiment_analysis(text) or sentiment_analyzer(text)[0]['label'])
                positive_count = df['Sentiment'].value_counts().get('POSITIVE', 0)
                total_count = len(df)
                score = (positive_count / total_count) * 100 if total_count > 0 else 0
                history.append({"Input": f"CSV Analysis - {text_column}", "Sentiment": f"{positive_count}/{total_count} POSITIVE", "Score": score, "Type": "CSV"})
                display(df)
                print(f"Sentiment Score: {score:.2f}/100")

        upload.observe(on_file_upload, names='value')
        display(upload)

# Function to view history
def on_view_history_click(b):
    with output:
        output.clear_output()
        if not history:
            print("No history available.")
        else:
            for entry in history:
                print(f"Input: {entry['Input']}\nSentiment: {entry['Sentiment']}\nScore: {entry['Score']:.2f}/100\nType: {entry['Type']}\n")

# Link buttons to functions
analyze_text_button.on_click(on_analyze_text_click)
analyze_csv_button.on_click(on_analyze_csv_click)
view_history_button.on_click(on_view_history_click)

# Display the interface
display(analyze_text_button, analyze_csv_button, view_history_button, output)
