import ipywidgets as widgets
from IPython.display import display, HTML
from transformers import pipeline
import random
import pandas as pd

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis') 

# Load the negative words from tamilbw.csv
tamil_badwords_df = pd.read_csv('tamilbw.csv', header=None)
tamil_badwords = tamil_badwords_df[0].tolist()  # Convert the words to a list

# Create an input box for the user to enter text with increased size and bold font
text_input = widgets.Textarea(
    value='',
    placeholder='TYPE YOUR TEXT HERE...',
    description='YOUR TEXT:',
    disabled=False,
    layout=widgets.Layout(width='100%', height='100px', margin='10px 0'),
    style={'font_family': 'Times New Roman', 'font_size': '24px', 'font_weight': 'bold', 'text_transform': 'uppercase'}
)

# Directly apply Impact font and golden color for the label
text_input.style.description_font = 'Impact'
text_input.style.description_color = 'gold'

# Create a button with a royal dark blue background and golden text, 3D effect
analyze_button = widgets.Button(
    description="ANALYZE SENTIMENT",
    layout=widgets.Layout(width='100%', height='50px', margin='10px 0'),
    style={'font_weight': 'bold', 'font_size': '24px', 'font_family': 'Times New Roman', 'text_transform': 'uppercase'},
)

# Directly override the button's background color to royal dark blue
analyze_button.style.button_color = "#00008B"  # Royal dark blue color

# Add custom class to button for golden text
analyze_button.add_class('golden-button')

# Output area to display sentiment results
output = widgets.Output()

# Function to handle analysis when the button is clicked
def on_button_click(b):
    with output:
        # Clear the previous output
        output.clear_output()

        # Get the user input text
        text = text_input.value.lower()  # Convert text to lowercase for easier matching

        # Check if any of the Tamil bad words exist in the user input
        for bad_word in tamil_badwords:
            if bad_word in text:
                sentiment = "NEGATIVE"
                score = 0.0  # Set a fixed negative score for simplicity
                response = generate_dynamic_response(sentiment, score)

                # Set the color and blink class for negative sentiment
                color = 'red'
                blink_class = 'negative-blink'

                # Display result with color and sentiment score
                display_sentiment(sentiment, score, color, blink_class, response)
                return  # Exit the function early once we find a match

        # If no Tamil bad word is found, perform standard sentiment analysis
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
display(HTML("""<style>
    /* Body and general layout */
    body {
        font-family: 'Times New Roman', serif;
        background: linear-gradient(to bottom, violet, black);
        background-size: 300% 300%;
        animation: moveBackground 5s ease infinite;
        color: white;
        padding: 20px;
        overflow: hidden;
    }
    @keyframes moveBackground {
        0% { background-position: 0 0; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0 0; }
    }
    /* Button and text input styling */
    .golden-button {
        background-color: #00008B;
        color: gold;
        font-weight: bold;
        font-size: 24px;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .golden-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3);
    }
    /* The result box styles */
    .output-box {
        padding: 20px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        border-radius: 10px;
        width: 100%;
        margin-top: 20px;
        animation-duration: 1s;
        animation-iteration-count: infinite;
        text-transform: uppercase;
        transition: all 0.5s ease-in-out;
    }
    /* Positive sentiment blinking effect */
    .positive-blink {
        background-color: #006400;
        border: 3px solid #006400;
        color: #00FF00;
        animation-name: blink-green;
        box-shadow: 0 10px 20px rgba(0, 255, 0, 0.5);
    }
    @keyframes blink-green {
        0% { background-color: #006400; color: #00FF00; }
        50% { background-color: #32CD32; color: #228B22; }
        100% { background-color: #006400; color: #00FF00; }
    }
    /* Negative sentiment blinking effect */
    .negative-blink {
        background-color: #8B0000;
        border: 3px solid #8B0000;
        color: #FF4500;
        animation-name: blink-red;
        box-shadow: 0 10px 20px rgba(255, 69, 0, 0.5);
    }
    @keyframes blink-red {
        0% { background-color: #8B0000; color: #FF4500; }
        50% { background-color: #B22222; color: #FF6347; }
        100% { background-color: #8B0000; color: #FF4500; }
    }
</style>"""))

# Display a 3D animated title
display(HTML('<div class="zoom-title">SENTIMENT ANALYSIS AI (NLP)</div>'))

# Display text input and button
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
