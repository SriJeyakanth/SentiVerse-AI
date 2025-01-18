import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
from transformers import pipeline
import google.generativeai as ai
import random
import time

# Configure Google Gemini API
API_KEY = 'AIzaSyCIgHspeOtytvBf0_ohZZdt43DUqNJBf2Q'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Load pre-trained sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# Predefined sentiment mapping
sentiment_mapping = {
    'nallathu': 'POSITIVE',
    'nalla': 'POSITIVE',
    'nanmai': 'POSITIVE',
    'pakka': 'POSITIVE',
    'nallavan': 'POSITIVE',
    'sandhosam': 'POSITIVE',
    'aanandham': 'POSITIVE',
    'super': 'POSITIVE',
    'semma': 'POSITIVE',
    'chanceless': 'POSITIVE',
    'magilchi': 'POSITIVE',
    'kettathu': 'NEGATIVE',
    'ketta': 'NEGATIVE',
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
    'otha': 'BAD WORD',
    'ngotha': 'BAD WORD',
    'thayoli': 'BAD WORD',
    'kai adi': 'BAD WORD',
    'maireey': 'BAD WORD',
    'kena': 'BAD WORD',
    'polayaadi moone': 'BAD WORD',
    'oombhu': 'BAD WORD',
    'nakku': 'BAD WORD',
    'kundi': 'BAD WORD',
    'soothu': 'BAD WORD',
    'sootha moodu': 'BAD WORD',
    'wakkalaoli': 'BAD WORD',
    'kunju': 'BAD WORD',
    'roudhiram': 'NEGATIVE',
    'paravala': 'NEUTRAL',
    'anyway good': 'NEUTRAL',
    'not bad': 'NEUTRAL',
    'need improvement': 'NEUTRAL',
    'needs improvement': 'NEUTRAL',
    'paravala': 'NEUTRAL',
    'anyway good': 'NEUTRAL',
    'not bad': 'NEUTRAL',
    'need improvement': 'NEUTRAL',
    'needs improvement': 'NEUTRAL',
    'okay': 'NEUTRAL',
    'fine': 'NEUTRAL',
    'alright': 'NEUTRAL',
    'nothing much': 'NEUTRAL',
    'just okay': 'NEUTRAL',
    'could be better': 'NEUTRAL',
    'could improve': 'NEUTRAL',
    'average': 'NEUTRAL',
    'neutral': 'NEUTRAL',
    'alright, I guess': 'NEUTRAL',
    'meh': 'NEUTRAL',
    'kinda okay': 'NEUTRAL',
    'moderate': 'NEUTRAL',
    'not great, not bad': 'NEUTRAL',
    'not perfect': 'NEUTRAL',
    'nothing to complain': 'NEUTRAL',
    'it’s fine': 'NEUTRAL',
    'acceptable': 'NEUTRAL',
    'more or less': 'NEUTRAL',
    'could do better': 'NEUTRAL',
    'just fine': 'NEUTRAL',
    'neither good nor bad': 'NEUTRAL',
    'a bit bland': 'NEUTRAL',
    'kinda dull': 'NEUTRAL',
    'nothing special': 'NEUTRAL',
    'in the middle': 'NEUTRAL',
    'not bad, not good': 'NEUTRAL',
    'more or less alright': 'NEUTRAL',
    'could be worse': 'NEUTRAL',
    'decent': 'NEUTRAL',
    'reasonably okay': 'NEUTRAL',
    'it’s alright': 'NEUTRAL',
    'no big deal': 'NEUTRAL',
    'mediocre': 'NEUTRAL',
    'not too exciting': 'NEUTRAL',
    'not amazing': 'NEUTRAL',
    'not disappointing': 'NEUTRAL',
    'it’s alright, nothing to complain': 'NEUTRAL',
    'just okay-ish': 'NEUTRAL',
    'feels neutral': 'NEUTRAL',
    'not bad, not amazing': 'NEUTRAL',
    'moderately good': 'NEUTRAL',
    'not spectacular': 'NEUTRAL',
    'it’ll do': 'NEUTRAL',
    'it’s decent enough': 'NEUTRAL',
    'so-so': 'NEUTRAL',
    'adequate': 'NEUTRAL',
    'could be improved': 'NEUTRAL',
    'not too bad': 'NEUTRAL',
    'shit': 'BAD WORD',
    'mairu': 'BAD WORD',

}

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
        "YOU SOUND RUDE! DO NOT USE BAD WORDS. IT IS MY WARNING!"
    ]

    if sentiment == 'POSITIVE':
        return random.choice(positive_responses)
    elif sentiment == 'NEGATIVE':
        return random.choice(negative_responses)
    elif sentiment == 'BAD WORD':
        return random.choice(bad_word_responses)
    else:
        return random.choice(neutral_responses)

# Function to show "thinking" message on the button itself
def show_loading_message_on_button():
    analyze_button.description = "SentiVerse AI is thinking..."

# Function to hide the "thinking" message on the button
def hide_loading_message_on_button():
    analyze_button.description = "ANALYZE SENTIMENT"

# Function to handle analysis when the button is clicked
def on_analyze_button_click(b):
    with output:
        # Show loading message on the button
        show_loading_message_on_button()

        # Clear previous output
        output.clear_output()

        # Get the user input text
        text = text_input.value.lower()  # Convert text to lowercase for easier matching

        # Check if any custom words exist in the input text
        for word, sentiment in sentiment_mapping.items():
            if word in text:
                score = 1.0
                response = generate_dynamic_response(sentiment, score)
                color = 'green' if sentiment == 'POSITIVE' else 'red'
                blink_class = 'positive-blink' if sentiment == 'POSITIVE' else 'negative-blink'
                display_sentiment(sentiment, score, color, blink_class, response)
                history.append((text, sentiment, response))
                hide_loading_message_on_button()  # Hide loading message on the button once the analysis is done
                return  # Exit if custom sentiment word is found

        # Simulate delay for AI response processing
        time.sleep(3)  # Simulate a delay in processing (this can be replaced with actual API call time)

        # Perform standard sentiment analysis if no custom word found
        result = sentiment_analyzer(text)
        sentiment = result[0]['label']
        score = result[0]['score']
        response = generate_dynamic_response(sentiment, score)

        # Now, generate a chat response from Gemini API based on sentiment
        chat_message = f"The sentiment of this feedback is {sentiment}. give business enhancing ideas according to this feedback in clear point by point.appreciate them with ideas if positive according to their situation.console them with ideas if they recieve negative or badword feedbacks.use more relevant emojis."
        ai_response = chat_response(chat_message)

        # Display sentiment and AI response
        color = 'green' if sentiment == 'POSITIVE' else 'red' if sentiment == 'NEGATIVE' else 'orange'
        blink_class = 'positive-blink' if sentiment == 'POSITIVE' else 'negative-blink'
        display_sentiment(sentiment, score, color, blink_class, response + "\nAI says: " + ai_response)

        history.append((text, sentiment, response + "\nAI says: " + ai_response))
        hide_loading_message_on_button()  # Hide loading message on the button once the analysis is done

# Function to display sentiment with color and blink effect
def display_sentiment(sentiment, score, color, blink_class, response):
    if sentiment == "POSITIVE":
        result_text = f"YOU'RE POSITIVE! 😊\nSENTIMENT: {sentiment}\n\n{response}"
    elif sentiment == "NEGATIVE":
        result_text = f"OH NO! NEGATIVE STUFF! 😞\nSENTIMENT: {sentiment}\n\n{response}"
    elif sentiment == "BAD WORD":
        result_text = f"BAD LANGUAGE DETECTED! 🚫\nSENTIMENT: {sentiment}\n\n{response}"
    else:  # Neutral sentiment case
        result_text = f"IT'S NEUTRAL. 🌟\nSENTIMENT: {sentiment}\n\n{response}"

    display(HTML(f""" 
    <div class="output-box {blink_class}" style="background-color: {color};"> 
        {result_text} 
    </div> 
    """))

# Function to handle viewing history when the button is clicked
def on_view_history_button_click(b):
    with output:
        # Clear previous output
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

# Function to handle chat responses using the Gemini API
def chat_response(user_message):
    try:
        response = chat.send_message(user_message)
        return response.text
    except ai.errors.ApiError as api_err:
        print(f"API Error: {api_err}")
    except Exception as e:
        print(f"Error: {e}")
    return "Sorry, something went wrong. Please try again."

# Attach the event handlers to the buttons
analyze_button.on_click(on_analyze_button_click)
view_history_button.on_click(on_view_history_button_click)

# Display the input box, buttons, and output area
display(text_input, analyze_button, view_history_button, output)
