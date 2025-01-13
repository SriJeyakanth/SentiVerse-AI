import ipywidgets as widgets
from IPython.display import display, HTML
from transformers import pipeline
import pandas as pd
import random

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# Load sentiment word files
positive_words = pd.read_csv('positive.csv')
negative_words = pd.read_csv('negative.csv')
tamil_words = pd.read_csv('tamilbw.csv')

# Create an input box for the user to enter text
text_input = widgets.Textarea(
    value='',
    placeholder='TYPE YOUR TEXT HERE...',
    description='YOUR TEXT:',
    disabled=False,
    layout=widgets.Layout(width='100%', height='100px', margin='10px 0'),
    style={'font_family': 'Times New Roman', 'font_size': '24px', 'font_weight': 'bold', 'text_transform': 'uppercase'}
)

# Create a button for analyzing sentiment
analyze_button = widgets.Button(
    description="ANALYZE SENTIMENT",
    layout=widgets.Layout(width='100%', height='50px', margin='10px 0'),
    style={'font_weight': 'bold', 'font_size': '24px', 'font_family': 'Times New Roman', 'text_transform': 'uppercase'},
)

# Output area to display sentiment results
output = widgets.Output()

# Function to handle analysis when the button is clicked
def on_button_click(b):
    with output:
        # Clear the previous output
        output.clear_output()

        # Get the user input text
        text = text_input.value.lower()  # Convert text to lowercase for easier matching

        # Define custom mappings for specific words to sentiments
        sentiment_mapping = {
            'nallathu': 'POSITIVE', 'nallavan': 'POSITIVE', 'sandhosam': 'POSITIVE',
            'aanandham': 'POSITIVE', 'super': 'POSITIVE', 'semma': 'POSITIVE',
            'chanceless': 'POSITIVE', 'magilchi': 'POSITIVE', 'kettathu': 'NEGATIVE',
            'mosam': 'NEGATIVE', 'drogram': 'NEGATIVE', 'kobam': 'NEGATIVE', 'erichal': 'NEGATIVE',
            'aathiram': 'NEGATIVE', 'koothi': 'NEGATIVE', 'sunni': 'NEGATIVE', 'punda': 'NEGATIVE',
            'pundamavane': 'NEGATIVE', 'othalaka': 'NEGATIVE', 'roudhiram': 'NEGATIVE',
            'paravala': 'NEUTRAL', 'anyway good': 'NEUTRAL', 'not bad': 'NEUTRAL',
            'need improvement': 'NEUTRAL', 'needs improvement': 'NEUTRAL'
        }

        # Check if any of the custom words exist in the user input
        for word, sentiment in sentiment_mapping.items():
            if word in text:
                # Assign sentiment and set a neutral score for simplicity
                score = 1.0  # You can adjust this based on preference
                response = generate_dynamic_response(sentiment, score)

                # Set the color and blink class based on sentiment
                if sentiment == 'POSITIVE':
                    color = 'green'
                    blink_class = 'positive-blink'
                elif sentiment == 'NEGATIVE':
                    color = 'red'
                    blink_class = 'negative-blink'
                else:
                    color = 'orange'  # Neutral color
                    blink_class = ''

                # Display result with color and sentiment score
                display_sentiment(sentiment, score, color, blink_class, response)
                return  # Exit the function early once we match a custom word

        # If no custom word is found, perform standard sentiment analysis
        result = sentiment_analyzer(text)
        sentiment = result[0]['label']
        score = result[0]['score']

        # Get response based on sentiment analysis
        response = generate_dynamic_response(sentiment, score)

        # Set the color based on sentiment
        if sentiment == 'POSITIVE':
            color = 'green'
            blink_class = 'positive-blink'
        else:
            color = 'red'
            blink_class = 'negative-blink'

        # Display result with color and sentiment score
        display_sentiment(sentiment, score, color, blink_class, response)

# Link the button click event to the function
analyze_button.on_click(on_button_click)

# Display the widgets (input box and button)
display(text_input, analyze_button, output)

# Generate a dynamic response based on sentiment
def generate_dynamic_response(sentiment, score):
    if sentiment == 'POSITIVE':
        responses = [
            "You're on top of the world! Keep spreading the positivity! 😄🌞",
            "What a wonderful mood! You're glowing with happiness! ✨🌻",
            "Keep shining, you're making the world brighter! 🌟💛"
        ]
    elif sentiment == 'NEGATIVE':
        responses = [
            "Don't let the storm clouds rain on your day. You got this! ⛈️🌈",
            "Mind your words, positivity will brighten your world 💬💖",
            "Don't let negativity consume you, you're stronger than this! 💪🌟"
        ]
    else:  # For Neutral sentiment
        responses = [
            "Things are steady, nothing to worry about. Just keep going. 😊",
            "It’s a neutral day, take it easy and stay balanced. ✨",
            "No strong emotions today, but you’re doing just fine. 🌿"
        ]

    # Pick a random response from the list to avoid repetition
    return random.choice(responses)

# Function to display the result with styled sentiment output
def display_sentiment(sentiment, score, color, blink_class, response):
    # Engaging text for sentiment result
    if sentiment == "POSITIVE":
        result_text = f"YOU'RE POSITIVE! 😊\nSENTIMENT: {sentiment}\n\n{response}"
    elif sentiment == "NEGATIVE":
        result_text = f"OH NO! SOMETHING SEEMS OFF! 😞\nSENTIMENT: {sentiment}\n\n{response}"
    else:
        result_text = f"IT'S NEUTRAL. 🌟\nSENTIMENT: {sentiment}\n\n{response}"

    # Display the output box with a blinking effect or normal neutral display
    display(HTML(f"""
        <div class="output-box {blink_class}" style="background-color: {color};">
            {result_text}
        </div>
    """))
