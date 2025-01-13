# Install necessary libraries if not already installed
!pip install transformers ipywidgets pandas

# Import necessary libraries
import pandas as pd
import random
import io
from transformers import pipeline
import ipywidgets as widgets
from IPython.display import display

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# Create buttons for the initial options
analyze_text_button = widgets.Button(
    description="ANALYZE TEXT",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)

analyze_csv_button = widgets.Button(
    description="ANALYZE CSV",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)

# Output area to display widgets dynamically
output = widgets.Output()

# Function to generate a dynamic response based on sentiment
def generate_dynamic_response(sentiment, score):
    if sentiment == 'POSITIVE':
        responses = [
            "You're on top of the world! Keep spreading the positivity! 😊",
            "What a wonderful mood! You're glowing with happiness! ✨",
            "Keep shining, you're making the world brighter! 💛"
        ]
    elif sentiment == 'NEGATIVE':
        responses = [
            "Don't let the storm clouds rain on your day. You got this! 🌈",
            "Mind your words, positivity will brighten your world 💬",
            "Don't let negativity consume you, you're stronger than this! 🌟"
        ]
    else:  # For Neutral sentiment
        responses = [
            "Things are steady, nothing to worry about. Just keep going. 😊",
            "It’s a neutral day, take it easy and stay balanced. ✨",
            "No strong emotions today, but you’re doing just fine. 🌿"
        ]

    # Pick a random response from the list to avoid repetition
    return random.choice(responses)

# Function to display the result
def display_sentiment(sentiment, score, response):
    print(f"SENTIMENT: {sentiment}\n\n{response}")

# Function to handle text analysis
def on_analyze_text_click(b):
    with output:
        output.clear_output()
        
        # Create an input box for the user to enter text
        text_input = widgets.Textarea(
            value='',
            placeholder='Type your text here...',
            layout=widgets.Layout(width='100%', height='100px', margin='10px 0')
        )

        # Create a button to analyze sentiment
        analyze_button = widgets.Button(
            description="Analyze Sentiment",
            layout=widgets.Layout(width='100%', height='50px', margin='10px 0')
        )

        # Function to handle analysis when the button is clicked
        def on_button_click(b):
            with output:
                output.clear_output()

                text = text_input.value.lower()  # Convert text to lowercase for easier matching

                # Custom word mappings for sentiment analysis
                sentiment_mapping = {
                    'nallathu': 'POSITIVE', 'nallavan': 'POSITIVE', 'sandhosam': 'POSITIVE',
                    'aanandham': 'POSITIVE', 'super': 'POSITIVE', 'semma': 'POSITIVE',
                    'chanceless': 'POSITIVE', 'magilchi': 'POSITIVE', 'kettathu': 'NEGATIVE',
                    'mosam': 'NEGATIVE', 'drogram': 'NEGATIVE', 'kobam': 'NEGATIVE',
                    'erichal': 'NEGATIVE', 'aathiram': 'NEGATIVE', 'koothi': 'NEGATIVE',
                    'sunni': 'NEGATIVE', 'punda': 'NEGATIVE', 'paravala': 'NEUTRAL',
                    'anyway good': 'NEUTRAL', 'not bad': 'NEUTRAL', 'need improvement': 'NEUTRAL',
                }

                for word, sentiment in sentiment_mapping.items():
                    if word in text:
                        score = 1.0
                        response = generate_dynamic_response(sentiment, score)
                        display_sentiment(sentiment, score, response)
                        return

                # Standard sentiment analysis if no match is found
                result = sentiment_analyzer(text)
                sentiment = result[0]['label']
                score = result[0]['score']
                response = generate_dynamic_response(sentiment, score)
                display_sentiment(sentiment, score, response)

        analyze_button.on_click(on_button_click)
        display(text_input, analyze_button)

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
                df = pd.read_csv(io.StringIO(content.decode('utf-8')))

                text_column = 'Text' if 'Text' in df.columns else df.columns[0]
                df['Sentiment'] = df[text_column].apply(
                    lambda text: sentiment_analyzer(text)[0]['label']
                )

                positive_count = df['Sentiment'].value_counts().get('POSITIVE', 0)
                total_count = len(df)
                score = (positive_count / total_count) * 100 if total_count > 0 else 0

                display(df)
                print(f"Sentiment Score: {score:.2f} out of 100")

        upload.observe(on_file_upload, names='value')
        display(upload)

# Link buttons to functions
analyze_text_button.on_click(on_analyze_text_click)
analyze_csv_button.on_click(on_analyze_csv_click)

# Display the interface
display(analyze_text_button, analyze_csv_button, output)
