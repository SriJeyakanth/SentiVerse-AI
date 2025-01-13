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

# Create a button for viewing history
view_history_button = widgets.Button(
    description="VIEW HISTORY",
    layout=widgets.Layout(width='100%', height='50px', margin='10px 0'),
    style={'font_weight': 'bold', 'font_size': '24px', 'font_family': 'Times New Roman', 'text_transform': 'uppercase'},
)

# Output area to display sentiment results and history
output = widgets.Output()

# Define custom mappings for specific words to sentiments
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
    'koothi': 'BAD WORD',
    'sunni': 'BAD WORD',
    'bastard': 'BAD WORD',
    'fuck': 'BAD WORD',
    'son of bitch': 'BAD WORD',
    'dick': 'BAD WORD',
    'fuck off': 'BAD WORD',
    'punda': 'BAD WORD',
    'pundamavane': 'BAD WORD',
    'othalaka': 'BAD WORD',
    'roudhiram': 'NEGATIVE',
    'paravala': 'NEUTRAL',
    'anyway good': 'NEUTRAL',
    'not bad': 'NEUTRAL',
    'need improvement': 'NEUTRAL',
    'needs improvement': 'NEUTRAL',
    'shit': 'BAD WORD'
}

# List to store history of activities
history = []

# Function to generate dynamic response based on sentiment and score
def generate_dynamic_response(sentiment, score):
    positive_responses = [
        "You're on top of the world! Keep spreading the positivity! 😄🌞",
        "What a wonderful mood! You're glowing with happiness! ✨🌻",
        "Keep shining, you're making the world brighter! 🌟💛"
    ]

    negative_responses = [
        "It seems like your text reflects some negative emotions. I hope things get better soon.",
        "Stay strong; tough times don’t last, but tough people do.",
        "It's okay to feel down sometimes. Take a deep breath, and things will improve."
    ]

    neutral_responses = [
        "Things are steady, nothing to worry about. Just keep going. 😊",
        "It’s a neutral day, take it easy and stay balanced. ✨",
        "No strong emotions today, but you’re doing just fine. 🌿"
    ]

    bad_word_responses = [
        "WARNING: Please avoid using inappropriate language. 🚫",
        "ALERT: The words you've used are not acceptable. ⚠️",
        "CAUTION: Inappropriate language detected! ⚠️",
        "PLEASE REFRAIN FROM USING SUCH WORDS. 🚫",
        "YOU SOUND RUDE ! DO NOT USE BAD WORDS.IT IS MY WARNING !"
    ]

    if sentiment == 'POSITIVE':
        return random.choice(positive_responses)
    elif sentiment == 'NEGATIVE':
        return random.choice(negative_responses)
    elif sentiment == 'BAD WORD':
        return random.choice(bad_word_responses)
    else:
        return random.choice(neutral_responses)

# Function to display sentiment with color and blink effect
def display_sentiment(sentiment, score, color, blink_class, response):
    # Engaging text for sentiment result
    if sentiment == "POSITIVE":
        result_text = f"YOU'RE POSITIVE! 😊\nSENTIMENT: {sentiment}\n\n{response}"
    elif sentiment == "NEGATIVE":
        result_text = f"OH NO! NEGATIVE STUFF! 😞\nSENTIMENT: {sentiment}\n\n{response}"
    elif sentiment == "BAD WORD":
        result_text = f"BAD LANGUAGE DETECTED! 🚫\nSENTIMENT: {sentiment}\n\n{response}"
    else:
        result_text = f"IT'S NEUTRAL. 🌟\nSENTIMENT: {sentiment}\n\n{response}"

    # Display the output box with a blinking effect or normal neutral display
    display(HTML(f""" 
    <div class="output-box {blink_class}" style="background-color: {color};"> 
        {result_text} 
    </div> 
    """))

# Function to handle analysis when the button is clicked
def on_analyze_button_click(b):
    with output:
        # Clear the previous output
        output.clear_output()
        # Get the user input text
        text = text_input.value.lower()  # Convert text to lowercase for easier matching

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
                elif sentiment == 'NEGATIVE' or sentiment == 'BAD WORD':
                    color = 'red'
                    blink_class = 'negative-blink'
                else:
                    color = 'orange'  # Neutral color
                    blink_class = ''
                # Display result with color and sentiment score
                display_sentiment(sentiment, score, color, blink_class, response)
                # Add to history
                history.append((text, sentiment, response))
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
        # Add to history
        history.append((text, sentiment, response))

# Function to handle viewing history when the button is clicked
def on_view_history_button_click(b):
    with output:
        # Clear the previous output
        output.clear_output()
        # Display history
        if history:
            for entry in history:
                text, sentiment, response = entry
                display(HTML(f"""
                <div style="margin-bottom: 10px;">
                    <strong>Text:</strong> {text}<br>
                    <strong>Sentiment:</strong> {sentiment}<br>
                    <strong>Response:</strong> {response}
                </div>
                """))
        else:
            display(HTML("<div>No history available.</div>"))

# Attach the event handlers to the buttons
analyze_button.on_click(on_analyze_button_click)
view_history_button.on_click(on_view_history_button_click)

# Display the input box, buttons, and output area
display(text_input, analyze_button, view_history_button, output)
