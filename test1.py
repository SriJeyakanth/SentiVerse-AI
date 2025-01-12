# Import required libraries
import ipywidgets as widgets
from IPython.display import display, HTML
from transformers import pipeline
import matplotlib.pyplot as plt
import pandas as pd

# Load sentiment analysis pipeline (using 'distilbert-base-uncased' for better English performance)
sentiment_analyzer = pipeline('sentiment-analysis')

def show_welcome_page():
    # Show the welcome page content
    welcome_html = """
    <div style="text-align: center; background: linear-gradient(to bottom right, green, black); height: 100vh; color: gold; font-family: 'Times New Roman', serif;">
        <h1 style="font-size: 60px; text-shadow: 2px 2px 5px rgba(255, 215, 0, 0.7); animation: zoom-in-out 2s infinite;">Welcome to Sentiment Analysis AI (NLP)</h1>
        <p style="font-size: 24px; padding: 10px 20px; animation: fade-in 2s;">Your personal assistant for analyzing text sentiment!</p>
        <button id="enter-btn" style="font-size: 24px; background-color: gold; color: black; padding: 10px 30px; cursor: pointer; border: none; font-weight: bold; animation: button-hover 1s infinite;">Enter NLP Model</button>
    </div>
    <style>
        @keyframes zoom-in-out {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        @keyframes fade-in {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        @keyframes button-hover {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
    """
    display(HTML(welcome_html))

    # Create the Enter NLP button
    enter_button = widgets.Button(description="Enter NLP Model", style={'font_weight': 'bold', 'font_size': '24px'})
    display(enter_button)

    # Function to transition to the next page (hide welcome and show sentiment analysis UI)
    def on_enter_button_click(b):
        # Hide the welcome page and show the sentiment analysis page
        enter_button.layout.display = 'none'  # Hide the button
        display(HTML('<div class="zoom-title">SENTIMENT ANALYSIS AI (NLP)</div>'))  # Title
        # Display the existing widgets
        display(text_input, analyze_button, analytics_button, output)

    # Link the button click to transition function
    enter_button.on_click(on_enter_button_click)

# Create an input box for the user to enter text with increased size, bold font, and Times New Roman font
text_input = widgets.Textarea(
    value='',
    placeholder='TYPE YOUR TEXT HERE...',
    description='YOUR TEXT:',
    disabled=False,
    layout=widgets.Layout(width='100%', height='150px', margin='10px 0'),
    style={'font_family': 'Times New Roman', 'font_size': '30px', 'font_weight': 'bold', 'text_transform': 'uppercase'}
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

# Button for viewing analytics
analytics_button = widgets.Button(
    description="VIEW ANALYTICS",
    layout=widgets.Layout(width='100%', height='50px', margin='20px 0'),  # Increased margin to add spacing
    style={'font_weight': 'bold', 'font_size': '24px', 'font_family': 'Times New Roman', 'text_transform': 'uppercase'},
)

# Output area to display sentiment results
output = widgets.Output()

# Initialize a list to store sentiment results for analytics
sentiment_history = []

# Function to handle analysis when the button is clicked
def on_button_click(b):
    with output:
        # Clear the previous output
        output.clear_output()

        # Get the user input text
        text = text_input.value

        # Analyze sentiment using the default model
        result = sentiment_analyzer(text)
        sentiment = result[0]['label']
        score = result[0]['score']

        # Handle the case where sentiment classification may be "NEUTRAL"
        if score < 0.6:  # If the confidence score is too low, classify as neutral
            sentiment = 'NEUTRAL'

        # Store the result in the sentiment history
        sentiment_history.append((sentiment, score))

        # Get response based on sentiment analysis
        response = generate_dynamic_response(sentiment, score)

        # Set the color based on sentiment
        if sentiment == 'POSITIVE':
            color = 'green'
            blink_class = 'positive-blink'
        elif sentiment == 'NEGATIVE':
            color = 'red'
            blink_class = 'negative-blink'
        else:
            color = 'yellow'
            blink_class = 'neutral-blink'

        # Display result with color and sentiment score
        display_sentiment(sentiment, score, color, blink_class, response)

# Link the button click event to the function
analyze_button.on_click(on_button_click)

# Function to display the analytics (Bar Graph, Scatter Plot, and Pie Chart)
def display_analytics(b):
    if not sentiment_history:
        print("No sentiment data available yet.")
        return

    # Convert sentiment history to a DataFrame for easy processing
    sentiment_df = pd.DataFrame(sentiment_history, columns=['Sentiment', 'Score'])

    # Create the Bar Graph: Sentiment counts
    sentiment_counts = sentiment_df['Sentiment'].value_counts()
    plt.figure(figsize=(8, 4))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'yellow'])
    plt.title('Sentiment Count')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

    # Create the Scatter Plot: Sentiment vs. Score
    plt.figure(figsize=(8, 4))
    colors = {'POSITIVE': 'green', 'NEGATIVE': 'red', 'NEUTRAL': 'yellow'}
    plt.scatter(sentiment_df.index, sentiment_df['Score'], c=sentiment_df['Sentiment'].map(colors), alpha=0.7)
    plt.title('Sentiment Score vs. Sentiment')
    plt.xlabel('Index')
    plt.ylabel('Sentiment Score')
    plt.show()

    # Create the Pie Chart: Sentiment distribution
    sentiment_pie = sentiment_df['Sentiment'].value_counts()
    plt.figure(figsize=(6, 6))
    sentiment_pie.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['green', 'red', 'yellow'])
    plt.title('Sentiment Distribution')
    plt.ylabel('')
    plt.show()

# Button for viewing analytics with a 3D golden yellow effect and thick black text
analytics_button = widgets.Button(
    description="VIEW ANALYTICS",
    layout=widgets.Layout(width='100%', height='50px', margin='20px 0'),  # Increased margin to add spacing
    style={'font_weight': 'bold', 'font_size': '24px', 'font_family': 'Times New Roman', 'text_transform': 'uppercase'},
)

# Apply custom styles directly to the button
analytics_button.style.button_color = "#FFD700"  # Golden yellow color for background
analytics_button.style.font_weight = 'bold'  # Bold text
analytics_button.style.font_size = '24px'  # Set font size
analytics_button.style.font_family = 'Times New Roman'  # Set font family
analytics_button.style.color = "#000000"  # Thick black text color

# Adding custom class for 3D effect on hover and button style
analytics_button.add_class('golden-3d-button')

# Button for viewing analytics function (same as before)
def display_analytics(b):
    if not sentiment_history:
        print("No sentiment data available yet.")
        return

    # Convert sentiment history to a DataFrame for easy processing
    sentiment_df = pd.DataFrame(sentiment_history, columns=['Sentiment', 'Score'])

    # Create the Bar Graph: Sentiment counts
    sentiment_counts = sentiment_df['Sentiment'].value_counts()
    plt.figure(figsize=(8, 4))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'yellow'])
    plt.title('Sentiment Count')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

    # Create the Scatter Plot: Sentiment vs. Score
    plt.figure(figsize=(8, 4))
    colors = {'POSITIVE': 'green', 'NEGATIVE': 'red', 'NEUTRAL': 'yellow'}
    plt.scatter(sentiment_df.index, sentiment_df['Score'], c=sentiment_df['Sentiment'].map(colors), alpha=0.7)
    plt.title('Sentiment Score vs. Sentiment')
    plt.xlabel('Index')
    plt.ylabel('Sentiment Score')
    plt.show()

    # Create the Pie Chart: Sentiment distribution
    sentiment_pie = sentiment_df['Sentiment'].value_counts()
    plt.figure(figsize=(6, 6))
    sentiment_pie.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['green', 'red', 'yellow'])
    plt.title('Sentiment Distribution')
    plt.ylabel('')
    plt.show()

# Link the "VIEW ANALYTICS" button to the function
analytics_button.on_click(display_analytics)

# Add the required CSS for 3D effect
display(HTML("""
    <style>
        /* 3D Effect for the Golden Yellow Button */
        .golden-3d-button {
            background-color: #FFD700;  /* Golden yellow color */
            color: #000000;  /* Black text */
            font-family: 'Times New Roman', serif;
            font-weight: bold;
            font-size: 24px;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);  /* Shadow for 3D effect */
            transition: all 0.3s ease;
            text-transform: uppercase;
        }

        /* Hover effect to enhance the 3D button look */
        .golden-3d-button:hover {
            transform: translateY(-5px);
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3);  /* Stronger shadow */
        }
    </style>
"""))


# Display the widgets (input box, buttons, and output area)
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
            font-size: 30px;  /* Increased font size */
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
            margin-top: 40px;  /* Added margin-top to give space between result and analytics */
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

        /* Neutral sentiment blinking effect */
        .neutral-blink {
            background-color: #FFD700;
            border: 3px solid #FFD700;
            color: #000000;
            animation-name: blink-neutral;
            box-shadow: 0 10px 20px rgba(255, 215, 0, 0.5);
            transform: rotateX(0deg) rotateY(0deg);
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

        @keyframes blink-neutral {
            0% { background-color: #FFD700; color: #000000; }
            50% { background-color: #FFFF00; color: #000000; }
            100% { background-color: #FFD700; color: #000000; }
        }

        /* Zoom in/out animation for the title */
        .zoom-title {
            font-family: 'Impact', sans-serif;
            font-size: 50px;
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

        /* Watermark at the bottom of the page */
        .watermark {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Times New Roman', serif;
            font-size: 16px;
            color: gold;
            opacity: 0.6;
            text-align: center;
        }
    </style>
"""))

# Display a 3D animated title
display(HTML('<div class="zoom-title">SENTIMENT ANALYSIS AI (NLP)</div>'))

# Display the text input, buttons, and output area
display(text_input, analyze_button, analytics_button, output)

# Display the watermark
display(HTML('<div class="watermark">TRAINED AND DEVELOPED BY K.SRI JEYAKANTH (AI ENTHUSIAST)</div>'))
