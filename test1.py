# Import required libraries
import ipywidgets as widgets
from IPython.display import display, HTML
from transformers import pipeline
import random

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

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
        text = text_input.value

        # Analyze sentiment
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
display(HTML("""
    <style>
        /* Body and general layout */
        body {
            font-family: 'Times New Roman', serif;
            background: linear-gradient(to bottom, violet, black);  /* Static gradient */
            background-size: 300% 300%;  /* This will make the gradient large for the animation */
            animation: moveBackground 5s ease infinite;  /* Faster background animation */
            color: white;
            padding: 20px;
            overflow: hidden;
        }

        /* Keyframes for moving the background */
        @keyframes moveBackground {
            0% {
                background-position: 0 0;
            }
            50% {
                background-position: 100% 100%;
            }
            100% {
                background-position: 0 0;
            }
        }

        /* Text input */
        .textarea {
            font-family: 'Times New Roman', serif;
            font-size: 24px;
            font-weight: bold;
            text-transform: uppercase;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #ccc;
            margin: 10px 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.2);  /* Slight transparency for text box */
            color: gold; /* Set the color to gold for the input text */
        }

        /* "YOUR TEXT" label styling */
        .textarea-label {
            font-family: 'Impact', sans-serif;
            font-size: 28px;
            font-weight: bold;
            color: gold;
            text-transform: uppercase;
            text-shadow: 2px 2px 5px rgba(255, 215, 0, 0.7); /* Golden shadow */
        }

        /* Button styling */
        .golden-button {
            background-color: #00008B;  /* Royal dark blue */
            color: gold;  /* Set text color to gold */
            font-family: 'Times New Roman', serif;
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

        /* Hover effect for the button */
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
            transform: rotateX(0deg) rotateY(15deg);
        }

        /* Negative sentiment blinking effect */
        .negative-blink {
            background-color: #8B0000;
            border: 3px solid #8B0000;
            color: #FF4500;
            animation-name: blink-red;
            box-shadow: 0 10px 20px rgba(255, 69, 0, 0.5);
            transform: rotateX(0deg) rotateY(-15deg);
        }

        /* Keyframes for blinking */
        @keyframes blink-green {
            0% { background-color: #006400; color: #00FF00; }
            50% { background-color: #32CD32; color: #228B22; }
            100% { background-color: #006400; color: #00FF00; }
        }

        @keyframes blink-red {
            0% { background-color: #8B0000; color: #FF4500; }
            50% { background-color: #B22222; color: #FF6347; }
            100% { background-color: #8B0000; color: #FF4500; }
        }

        /* Result text styles */
        .output-box {
            font-family: 'Impact', sans-serif;
            color: black;
            font-weight: bold;
            font-size: 30px;
        }

        /* 3D animation effect */
        .textarea, .golden-button {
            transform-style: preserve-3d;
            perspective: 1000px;
        }

        .textarea:hover, .golden-button:hover {
            transform: rotateY(20deg);
            transition: transform 0.5s ease-in-out;
        }

        /* Zoom in/out animation for the title */
        .zoom-title {
            font-family: 'Impact', sans-serif;
            font-size: 50px;  /* Slightly reduced size */
            font-weight: bold;
            color: gold;
            text-align: center;
            animation: zoom-in-out 2s infinite;
            text-transform: uppercase;
            text-shadow: 3px 3px 10px rgba(255, 215, 0, 0.7);
        }

        /* Keyframes for the zooming effect */
        @keyframes zoom-in-out {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
            }
            100% {
                transform: scale(1);
            }
        }

    </style>
"""))

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
    else:
        responses = [
            "Don't let the storm clouds rain on your day. You got this! ⛈️🌈",
            "Mind your words, positivity will brighten your world 💬💖",
            "Don't let negativity consume you, you're stronger than this! 💪🌟"
        ]

    # Pick a random response from the list to avoid repetition
    return random.choice(responses)

# Function to display the result with styled sentiment output
def display_sentiment(sentiment, score, color, blink_class, response):
    # Engaging text for sentiment result
    if sentiment == "POSITIVE":
        result_text = f"YOU'RE POSITIVE! 😊\nSENTIMENT: {sentiment}\nCONFIDENCE: {score:.2f}\n{response}"
    else:
        result_text = f"OH NO! SOMETHING SEEMS OFF! 😞\nSENTIMENT: {sentiment}\nCONFIDENCE: {score:.2f}\n{response}"

    # Display the output box with a blinking effect
    display(HTML(f"""
        <div class="output-box {blink_class}">
            {result_text}
        </div>
    """))
