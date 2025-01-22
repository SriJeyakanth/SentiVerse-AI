import pandas as pd
import io
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
import ipywidgets as widgets
from IPython.display import display, HTML

# Initialize sentiment analysis models
analyzer_vader = SentimentIntensityAnalyzer()

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
    'good but needs improvement': 'NEUTRAL',
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


# Custom CSS for styling
custom_css = """
<style>
    body {
        background: linear-gradient(to right, green, black);
        color: white;
    }
    .widget-box {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 20px;
        font-family: "Arial", sans-serif;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
    }
    .positive { background-color: green; color: white; }
    .negative { background-color: red; color: white; }
    .neutral { background-color: yellow; color: black; }
    .badword { background-color: red; color: white; animation: blink-red 1s infinite; }
    .loading {
        font-size: 50px;
        font-family: "Impact", sans-serif;
        text-align: center;
        color: white;
        animation: zoomInOut 1s infinite, colorChange 3s infinite;
        text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
        padding: 10px 0;
    }
    .score-display {
        font-size: 40px;
        color: white;
        font-family: "Impact", sans-serif;
        padding: 20px;
        text-align: center;
    }
    .positive-score {
        background-color: green;
        animation: blink-green 1s infinite;
    }
    .negative-score {
        background-color: red;
        animation: blink-red 1s infinite;
    }
    .neutral-score {
        background-color: yellow;
        animation: blink-yellow 1s infinite;
    }
    @keyframes blink-green {
        0%, 100% { background-color: green; }
        50% { background-color: lightgreen; }
    }
    @keyframes blink-red {
        0%, 100% { background-color: red; }
        50% { background-color: darkred; }
    }
    @keyframes blink-yellow {
        0%, 100% { background-color: yellow; }
        50% { background-color: lightyellow; }
    }
    @keyframes jump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .progress-bar {
        width: 100%;
        background-color: #ddd;
    }
    .progress-bar-fill {
        height: 30px;
        width: 0%;
        background-color: #4caf50;
        text-align: center;
        line-height: 30px;
        color: white;
        transition: width 0.5s;
    }
    .btn-custom {
        background: gold;
        color: black;
        font-weight: bold;
        border: none;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 5px #666;
        transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
    }
    .btn-custom:active {
        box-shadow: 0 2px #666;
        transform: translateY(4px);
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        font-size: 20px;
        font-weight: bold;
        color: black;
    }
    th {
        background-color: #f2f2f2;
        color: black;
    }
</style>
"""

display(HTML(custom_css))

# Helper Functions
def perform_sentiment_analysis(text):
    sentiment = sentiment_mapping.get(text, "NEUTRAL")
    score = 0.5

    if sentiment == "NEUTRAL":
        blob = TextBlob(text)
        polarity_tb = blob.sentiment.polarity

        sentiment_dict = analyzer_vader.polarity_scores(text)
        polarity_vader = sentiment_dict['compound']

        final_polarity = (polarity_tb + polarity_vader) / 2

        if final_polarity > 0:
            sentiment = "POSITIVE"
        elif final_polarity < 0:
            sentiment = "NEGATIVE"

    response = generate_dynamic_response(sentiment, score)
    return sentiment, score, response

def generate_dynamic_response(sentiment, score):
    responses = {

        'POSITIVE': [
            "You're on top of the world! Keep spreading positivity! 🌞",
            "What a wonderful mood! You're glowing with happiness! ✨",

    "Most of the things you've mentioned are positive! Keep it up! 🌟",
    "Your positivity is contagious! Keep shining bright! 🌟",
    "You're a beacon of light in a dark world. Keep radiating joy! ✨",
    "Success is within your reach. Keep pushing forward! 🚀",
    "Your determination is admirable. Keep striving for greatness! 🌠",
    "Your enthusiasm is inspiring! Keep the energy high! ⚡",
    "You’re doing an amazing job! Keep up the fantastic work! 👍",
    "Your smile lights up the room. Keep smiling! 😊",
    "You’re a rockstar! Keep rocking your goals! 🎸",
    "The world needs more people like you. Keep being awesome! 🌈",
    "You’ve got this! Keep smashing those targets! 💥",
    "Your hard work is paying off. Keep going! 🏆",
    "You’re unstoppable! Keep chasing your dreams! 🌄",
    "Your positive vibes are appreciated. Keep spreading them! 🌸",
    "Great job! Keep striving for excellence! 🥇",
    "Your efforts are making a difference. Keep making waves! 🌊",
    "You’re an inspiration! Keep inspiring others! 🌻",
    "Your dedication is commendable. Keep pursuing your passions! 🌟",
    "You’re amazing! Keep reaching new heights! ⛰️",
    "Your creativity is shining through. Keep creating! 🎨",
    "You’re a game-changer! Keep changing the world! 🌍",
    "Your kindness is making the world better. Keep being kind! 🌼",
    "You’re a positive force. Keep making an impact! 💫",
    "You’re doing a fantastic job! Keep the momentum going! 🚀",
    "Your resilience is inspiring. Keep bouncing back! 🏅",
    "You’re a trailblazer! Keep forging new paths! 🌟",
    "Your determination is leading you to success. Keep it up! 🌠",
    "You’re incredible! Keep being your awesome self! 🎉",
    "You’re making great strides. Keep moving forward! 🏃",
    "Your positive attitude is infectious. Keep spreading joy! 😄",
    "You’re a superstar! Keep shining bright! 🌟",
    "Your hard work is evident. Keep pushing through! 💪",
    "You’re an amazing leader. Keep leading with positivity! 🌟",
    "Your enthusiasm is uplifting. Keep the good vibes flowing! 🎈",
    "You’re a source of positivity. Keep inspiring others! 🌞",
    "Your energy is unmatched. Keep the fire burning! 🔥",
    "You’re making a big impact. Keep going strong! 💥",
    "Your persistence is paying off. Keep pushing boundaries! 🚀",
    "You’re a ray of sunshine! Keep brightening up the world! 🌞",
    "Your accomplishments are impressive. Keep achieving more! 🏆",
    "You’re doing a phenomenal job! Keep up the great work! 👍",
    "Your positivity is making a difference. Keep spreading joy! 🌸",
    "You’re an inspiration to many. Keep shining! ✨",
    "Your hard work and dedication are paying off. Keep it up! 🌟",
    "You’re a beacon of positivity. Keep lighting up the world! 🌟",
    "Your efforts are truly appreciated. Keep making an impact! 🌊",
    "You’re a rockstar! Keep shining bright! 🎸",
    "Your determination is leading you to success. Keep pushing! 🌠",
    "You’re amazing! Keep inspiring those around you! 🎉",
    "Your positive mindset is powerful. Keep spreading good vibes! 🌞",
    "You’re on the right path. Keep moving forward! 🚀",
    "Your energy is inspiring. Keep the momentum going! 💫",
    "You’re making a difference. Keep up the great work! 🌍",
    "Your hard work is evident. Keep striving for excellence! 🏆",
    "You’re a positive force. Keep making waves! 🌊",
    "Your resilience is commendable. Keep bouncing back! 🏅",
    "You’re a trailblazer! Keep forging new paths! 🌟",
    "Your determination is leading you to great heights. Keep it up! 🌠",
    "You’re incredible! Keep being your awesome self! 🎉",
    "You’re making great strides. Keep pushing forward! 🏃",
    "Your positive attitude is infectious. Keep spreading joy! 😄",
    "You’re a superstar! Keep shining bright! 🌟",
    "Your hard work is evident. Keep pushing through! 💪",
    "You’re an amazing leader. Keep leading with positivity! 🌟",
    "Your enthusiasm is uplifting. Keep the good vibes flowing! 🎈",
    "You’re a source of positivity. Keep inspiring others! 🌞",
    "Your energy is unmatched. Keep the fire burning! 🔥",
    "You’re making a big impact. Keep going strong! 💥",
    "Your persistence is paying off. Keep pushing boundaries! 🚀",
    "You’re a ray of sunshine! Keep brightening up the world! 🌞",
    "Your accomplishments are impressive. Keep achieving more! 🏆",
    "You’re doing a phenomenal job! Keep up the great work! 👍",
    "Your positivity is making a difference. Keep spreading joy! 🌸",
    "You’re an inspiration to many. Keep shining! ✨",
    "Your hard work and dedication are paying off. Keep it up! 🌟",
    "You’re a beacon of positivity. Keep lighting up the world! 🌟",
    "Your efforts are truly appreciated. Keep making an impact! 🌊",
    "You’re a rockstar! Keep shining bright! 🎸",
    "Your determination is leading you to success. Keep pushing! 🌠",
    "You’re amazing! Keep inspiring those around you! 🎉",
    "Your positive mindset is powerful. Keep spreading good vibes! 🌞",
    "You’re on the right path. Keep moving forward! 🚀",
    "Your energy is inspiring. Keep the momentum going! 💫",
    "You’re making a difference. Keep up the great work! 🌍",
    "Your hard work is evident. Keep striving for excellence! 🏆",
    "You’re a positive force. Keep making waves! 🌊",
    "Your resilience is commendable. Keep bouncing back! 🏅",
    "You’re a trailblazer! Keep forging new paths! 🌟",
    "Your determination is leading you to great heights. Keep it up! 🌠",
    "You’re incredible! Keep being your awesome self! 🎉",
    "You’re making great strides. Keep pushing forward! 🏃",
    "Your positive attitude is infectious. Keep spreading joy! 😄",
    "You’re a superstar! Keep shining bright! 🌟",
    "Your hard work is evident. Keep pushing through! 💪",
    "You’re an amazing leader. Keep leading with positivity! 🌟",
    "Your enthusiasm is uplifting. Keep the good vibes flowing! 🎈",
    "You’re a source of positivity. Keep inspiring others! 🌞",
    "Your energy is unmatched. Keep the fire burning! 🔥",
    "You’re making a big impact. Keep going strong! 💥",
    "Your persistence is paying off. Keep pushing boundaries! 🚀",
    "You’re a ray of sunshine! Keep brightening up the world! 🌞"
],

       'NEGATIVE': [
    "It seems like your text reflects some negative emotions. Stay strong. 💪",
    "It's okay to feel down sometimes. Take a deep breath, and things will improve. 🌈",
    "You're not alone. Things will get better. 🌟",
    "Hang in there. Tough times don't last. 💫",
    "Every storm runs out of rain. Keep your head up. ☔",
    "It's okay to feel this way. You're doing your best. 🌷",
    "Better days are coming. Just hold on a little longer. 🌅",
    "You’re stronger than you think. Keep pushing through. 🌠",
    "It's a rough patch, but you will get through it. 💪",
    "It's not easy right now, but you're tougher than you know. 🌱",
    "Stay strong. This too shall pass. 🌸",
    "Remember, it's okay to ask for help. You're not alone. 🤝",
    "Take it one day at a time. You’ve got this. 🗓️",
    "Courage doesn’t always roar. Sometimes it's the quiet voice at the end of the day saying, 'I will try again tomorrow.' 🌅",
    "You are more than your mistakes. Keep moving forward. 🌿",
    "Hard times are a part of life's journey. They make the good times better. 🌄",
    "It's okay to be sad. It’s part of being human. 🌺",
    "You’ve overcome challenges before. You can do it again. 🌟",
    "You’re stronger than the struggles you face. 💪",
    "It's okay to not be okay all the time. 🌈",
    "This is just a chapter, not the whole story. 📖",
    "You’re capable of amazing things. Keep going. 🚀",
    "You’re brave for facing these feelings. 🌻",
    "It's okay to feel lost sometimes. You'll find your way. 🗺️",
    "It’s a hard time now, but brighter days are ahead. 🌞",
    "You’re stronger with every challenge you face. 💥",
    "It's okay to take a break and recharge. 🛌",
    "Sometimes the hardest climb leads to the best views. 🌄",
    "You’re doing great. Keep going. 🌠",
    "It's a tough moment, but you are tougher. 💪",
    "You have the strength to get through this. 🌟",
    "It's okay to cry. Tears can be healing. 🌧️",
    "You are resilient. Keep pushing forward. 🌱",
    "Things will get better. Hang in there. 🌈",
    "You are important and your feelings matter. 🧡",
    "It's okay to feel overwhelmed. Take it step by step. 🚶",
    "You’re not alone in this. Lean on your support system. 🤝",
    "You are stronger than you think. 🌿",
    "It's okay to take it slow. Healing takes time. 🕰️",
    "You are capable of overcoming this. 💪",
    "It's just a tough day, not a tough life. 🌻",
    "You’re doing better than you think. Keep going. 🌟",
    "You are resilient and can handle this. 🌱",
    "This moment is temporary. Better days are ahead. 🌄",
    "You are loved and supported. Reach out if you need to. 💌",
    "It's okay to feel down. You’re human. 🌼",
    "You’ve got this. Keep pushing through. 💪",
    "It’s a rough time, but you will emerge stronger. 🌟",
    "You are doing your best, and that’s enough. 🌺",
    "It's okay to seek help. You don’t have to do it alone. 🤝",
    "You’re strong enough to get through this. 🌷",
    "It's okay to feel sad. Let yourself feel it. 🌧️",
    "You will rise above this. 🌅",
    "You have the strength to overcome this. 💪",
    "You’re doing great. Keep moving forward. 🌠",
    "It's a tough moment, but you are tougher. 🌱",
    "You are capable of amazing things. 🚀",
    "It's okay to not be okay. Take it one step at a time. 🗓️",
    "You are resilient. Keep fighting. 💪",
    "You are not defined by this moment. 🌸",
    "You are stronger than you feel. 💪",
    "It's okay to ask for support. 🤝",
    "You are doing your best, and that’s enough. 🌟",
    "You are capable of handling this. 🌿",
    "You are stronger than this challenge. 💪",
    "This moment is temporary. Keep going. 🌈",
    "You are important and your feelings matter. 🧡",
    "You have the strength to get through this. 🌱",
    "It's okay to feel overwhelmed. Take a breath. 🌬️",
    "You are capable of overcoming this. 💪",
    "You are resilient and strong. 🌟",
    "It's a tough time, but you are tougher. 💪",
    "You’ve got this. Keep going. 🌠",
    "It's okay to feel down. You’re human. 🌼",
    "You are loved and supported. Reach out. 💌",
    "This moment will pass. Stay strong. 💪",
    "You are resilient. Keep fighting. 🌱",
    "You are stronger than you think. 💪",
    "It’s okay to take it slow. Healing takes time. 🕰️",
    "You are capable of amazing things. 🚀",
    "You are doing better than you think. Keep going. 🌟",
    "You are resilient and strong. 💪",
    "This moment is temporary. Keep moving forward. 🌄",
    "You are important and your feelings matter. 🧡",
    "You are loved and supported. Reach out if you need to. 💌",
    "You are resilient and can handle this. 🌿",
    "It's okay to feel sad. Let yourself feel it. 🌧️",
    "You will rise above this. 🌅",
    "You have the strength to overcome this. 💪",
    "You are doing great. Keep moving forward. 🌠",
    "You are stronger than you feel. 💪",
    "It's okay to ask for support. 🤝",
    "You are doing your best, and that’s enough. 🌸",
    "You are capable of handling this. 🌱",
    "This moment is temporary. Better days are ahead. 🌈",
    "You are important and your feelings matter. 🧡",
    "It's okay to feel overwhelmed. Take a breath. 🌬️"
],

       'BAD WORD': [
    "WARNING: Please avoid using inappropriate language. 🚫",
    "ALERT: The words you've used are not acceptable. ⚠️",
    "Inappropriate language detected. Please refrain from using it. ❌",
    "Your language is flagged as inappropriate. Please use respectful words. 🙏",
    "Offensive language detected. Let's keep the conversation positive. 😊",
    "Inappropriate terms found. Please use appropriate language. 🛑",
    "Please avoid using such language. It's not acceptable. 🚫",
    "Detected offensive words. Let's keep it civil. 👌",
    "The language used is not acceptable. Please use respectful language. 🙏",
    "Offensive terms detected. Let's maintain a positive dialogue. 🌟",
    "Inappropriate language found. Please avoid using such words. ❌",
    "Offensive words detected. Please keep the conversation polite. 🤝",
    "The words used are flagged as inappropriate. Use respectful language. 🙏",
    "Please refrain from using offensive language. Let's keep it positive. 🌈",
    "Inappropriate words detected. Please use appropriate language. 🛑",
    "Your language is flagged as offensive. Let's keep the conversation civil. 😊",
    "Detected inappropriate language. Please avoid such terms. 🚫",
    "Offensive language found. Let's keep the conversation respectful. 👌",
    "Inappropriate terms detected. Please use respectful language. 🙏",
    "Your language is flagged as unacceptable. Let's keep it polite. 🌟",
    "Detected offensive terms. Please use appropriate language. 🚫",
    "Inappropriate words found. Let's maintain a positive dialogue. 😊",
    "Offensive terms detected. Please keep the conversation respectful. 🙏",
    "The language used is inappropriate. Please use respectful words. 🚫",
    "Offensive language detected. Let's keep the conversation positive. 🌟",
    "Inappropriate language found. Please refrain from using it. 🛑",
    "Your language is flagged as offensive. Please use respectful terms. 🤝",
    "Offensive words detected. Please keep the conversation civil. 🌈",
    "Detected inappropriate terms. Please use respectful language. 🚫",
    "The words used are flagged as offensive. Let's keep it positive. 🙏",
    "Please avoid using offensive language. It's not acceptable. 🚫",
    "Detected inappropriate language. Please use respectful words. 🌟",
    "Offensive terms found. Let's keep the conversation polite. 👌",
    "Inappropriate language detected. Please use appropriate terms. 🛑",
    "Your language is flagged as inappropriate. Please keep it civil. 😊",
    "Inappropriate terms detected. Please avoid using such words. 🚫",
    "Offensive words found. Let's maintain a positive dialogue. 🤝",
    "The language used is flagged as inappropriate. Please use respectful terms. 🙏",
    "Offensive language detected. Please keep the conversation respectful. 🌟",
    "Inappropriate words detected. Please use appropriate language. 🛑",
    "Your language is flagged as offensive. Let's keep it polite. 🚫",
    "Detected offensive language. Please use respectful words. 😊",
    "Inappropriate terms found. Let's maintain a positive dialogue. 🌈",
    "Offensive language detected. Please avoid using such words. 🚫",
    "The words used are flagged as offensive. Please use respectful terms. 🙏",
    "Detected inappropriate language. Please keep the conversation civil. 🌟",
    "Offensive terms detected. Please use appropriate language. 🚫",
    "Inappropriate words found. Let's keep the conversation respectful. 😊",
    "Your language is flagged as inappropriate. Let's keep it positive. 🚫",
    "Offensive language detected. Please avoid using it. 🛑",
    "The language used is flagged as inappropriate. Please keep it civil. 🤝",
    "Inappropriate terms detected. Please use respectful language. 🙏",
    "Offensive words detected. Let's maintain a positive dialogue. 🌟",
    "Detected inappropriate language. Please use respectful words. 🚫",
    "Offensive language found. Please keep the conversation respectful. 👌",
    "Your language is flagged as offensive. Please use appropriate terms. 🚫",
    "Detected offensive terms. Please avoid using such words. 😊",
    "Inappropriate language found. Please keep the conversation civil. 🌈",
    "Offensive terms detected. Please use respectful words. 🙏",
    "The language used is flagged as inappropriate. Please keep it positive. 🚫",
    "Offensive language detected. Please avoid using it. 🛑",
    "Inappropriate terms detected. Please use respectful language. 🤝",
    "Your language is flagged as inappropriate. Let's keep the conversation civil. 🌟",
    "Detected offensive language. Please use appropriate terms. 🚫",
    "Offensive words found. Let's maintain a positive dialogue. 😊",
    "Inappropriate language detected. Please keep the conversation respectful. 🚫",
    "Your language is flagged as offensive. Please avoid using such words. 🤝",
    "Offensive terms detected. Please use respectful language. 🌟",
    "The language used is flagged as inappropriate. Please keep it civil. 🚫",
    "Inappropriate terms found. Please keep the conversation respectful. 😊",
    "Offensive language detected. Let's maintain a positive dialogue. 🚫",
    "Your language is flagged as inappropriate. Please use respectful words. 🤝",
    "Inappropriate language detected. Let's keep the conversation polite. 🌟",
    "Offensive words found. Please avoid using such terms. 🚫",
    "Detected offensive language. Please use respectful language. 😊",
    "The words used are flagged as offensive. Please keep it civil. 🚫",
    "Inappropriate terms detected. Please use appropriate language. 🌟",
    "Offensive language found. Let's maintain a positive dialogue. 🚫",
    "Your language is flagged as inappropriate. Please keep it respectful. 🤝",
    "Offensive language detected. Please avoid using such words. 🌟",
    "Inappropriate words found. Let's keep the conversation polite. 🚫",
    "Detected offensive language. Please use respectful terms. 😊",
    "The words used are flagged as inappropriate. Please use respectful language. 🚫",
    "Offensive terms detected. Please keep the conversation civil. 🚫",
    "Inappropriate language detected. Let's maintain a positive dialogue. 😊",
    "Your language is flagged as offensive. Please avoid using such terms. 🤝"
],

        'NEUTRAL': [
    "Things are steady, nothing to worry about. Just keep going. 😊",
    "No strong emotions today, but you're doing just fine. 🌿",
    "All is calm and balanced. Keep it up! 🌻",
    "Everything's under control. Maintain your pace. 🌾",
    "Things are stable. You're doing great. 🏞️",
    "No big changes, but you're on the right track. 🌼",
    "Everything's in equilibrium. Keep it going. ⚖️",
    "Things are mellow. Just keep being you. 🌺",
    "You're doing a good job maintaining balance. 🌳",
    "No extremes today. You're steady and strong. 🚶",
    "Everything's in order. Keep up the good work. 📘",
    "Life is smooth sailing right now. Stay the course. 🚢",
    "All is well. You're in a good place. 🌴",
    "Things are settled. Keep up the steady progress. 🧘",
    "Everything's balanced. You're doing fine. ⚖️",
    "Life's cruising at a steady pace. Keep going. 🛣️",
    "Everything's even-keeled. Stay steady. 🚤",
    "You're maintaining good balance. Keep it up. 🏞️",
    "Things are consistent. Keep doing what you're doing. 🌿",
    "All is stable. You're on solid ground. 🏔️",
    "Everything's level. Keep up the good work. 📏",
    "No highs or lows, just a steady rhythm. Keep going. 🎶",
    "You're handling things well. Stay the course. 🚀",
    "Everything's smooth and balanced. Keep moving. 🛤️",
    "Life is calm. You're doing great. 🌄",
    "Everything's under control. Keep it steady. 🧭",
    "Things are going smoothly. Keep up the pace. 🌞",
    "All is even. You're doing just fine. 🌳",
    "Everything's in harmony. Keep it going. 🎼",
    "No major shifts, just a steady flow. Keep moving. 🌊",
    "You're maintaining stability. Keep it up. 🏡",
    "Everything's on an even keel. Stay steady. ⛵",
    "Life is balanced. Keep moving forward. 🌄",
    "Things are consistent. Keep doing your best. 🌼",
    "Everything's steady. You're doing well. 🌳",
    "No peaks or valleys, just a smooth ride. Keep going. 🚗",
    "You're doing a good job maintaining calm. 🧘",
    "Everything's in equilibrium. Keep it steady. ⚖️",
    "Life is even-keeled. Keep moving forward. 🚶",
    "Things are stable and balanced. Keep it up. 🌿",
    "All is level. You're on the right path. 🛣️",
    "Everything's calm. Stay the course. 🌞",
    "Life is mellow. You're doing just fine. 🌴",
    "Everything's under control. Keep moving forward. 🧭",
    "Things are in order. Keep up the good work. 📘",
    "No highs or lows, just a steady pace. Keep going. 🎶",
    "You're handling things well. Stay steady. 🚀",
    "Everything's balanced. Keep it up. ⚖️",
    "Life is smooth. Keep moving forward. 🚢",
    "Everything's on an even keel. Stay the course. ⛵",
    "Things are stable and steady. Keep it going. 🏡",
    "All is even. Keep up the steady progress. 🌾",
    "Everything's in harmony. Stay balanced. 🎼",
    "Life is calm and steady. Keep going. 🌄",
    "Everything's consistent. You're doing great. 🏞️",
    "Things are smooth. Keep up the good work. 🚗",
    "Everything's balanced. Keep moving forward. ⚖️",
    "No extremes today. You're doing well. 🚶",
    "Everything's under control. Maintain your pace. 🌾",
    "Life is balanced. Keep moving forward. 🏔️",
    "Things are even-keeled. Keep it up. 🚤",
    "Everything's in equilibrium. You're doing fine. 🏞️",
    "No big changes, just steady progress. Keep moving. 🌳",
    "You're maintaining balance. Keep it up. 🌿",
    "Everything's calm. Stay the course. 🧘",
    "Life is smooth. Keep going. 🚢",
    "Everything's steady. You're doing great. 🌾",
    "No highs or lows, just a steady rhythm. Keep moving. 🎶",
    "You're handling things well. Stay steady. 🚀",
    "Everything's in harmony. Keep it up. 🌼",
    "Life is balanced. Keep moving forward. ⚖️",
    "Things are consistent. Keep doing your best. 🌳",
    "Everything's even-keeled. Stay the course. ⛵",
    "All is level. Keep moving forward. 🚶",
    "Everything's calm and balanced. You're doing great. 🌞",
    "Life is mellow. Keep it going. 🌴",
    "Everything's under control. Maintain your pace. 🧭",
    "Things are smooth. Keep up the good work. 🚗",
    "Everything's balanced. Keep moving forward. 🌿",
    "No peaks or valleys, just a smooth ride. Keep going. 🚗",
    "You're doing a good job maintaining calm. 🧘",
    "Everything's in equilibrium. Keep it steady. ⚖️",
    "Life is even-keeled. Keep moving forward. 🚶",
    "Things are stable and balanced. Keep it up. 🌿",
    "All is level. You're on the right path. 🛣️",
    "Everything's calm. Stay the course. 🌞",
    "Life is mellow. You're doing just fine. 🌴"
],

    }
    return random.choice(responses.get(sentiment, ["Neutral feedback detected."]))

# Widgets for UI
analyze_csv_button = widgets.Button(
    description="ANALYZE CSV",
    layout=widgets.Layout(width='50%', height='50px', margin='10px 0')
)
analyze_csv_button.add_class('btn-custom')

output = widgets.Output()
loading_text = widgets.Label(
    value="THE SENTIVERSE AI IS ANALYZING YOUR FILE........",
    layout=widgets.Layout(width='100%', margin='10px 0')
)
loading_text.add_class('loading')

progress_bar = HTML('<div class="progress-bar"><div class="progress-bar-fill" style="width: 0%;">0%</div></div>')

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
        upload.add_class('btn-custom')

        def on_file_upload(change):
            with output:
                output.clear_output()
                display(loading_text)  # Display loading text
                display(progress_bar)  # Display progress bar

                uploaded_file = next(iter(upload.value.values()))
                content = uploaded_file['content']
                file_name = uploaded_file.get('name', 'Unknown File')
                df = pd.read_csv(io.StringIO(content.decode('utf-8')))

                text_column = 'Text' if 'Text' in df.columns else df.columns[0]
                total_entries = len(df)
                analyzed_count = 0

                def update_progress_bar(progress):
                    progress_percentage = int((progress / total_entries) * 100)
                    progress_bar.value = f'<div class="progress-bar"><div class="progress-bar-fill" style="width: {progress_percentage}%; line-height: 30px; color: white;">{progress_percentage}%</div></div>'

                sentiments = []
                for text in df[text_column]:
                    sentiments.append(perform_sentiment_analysis(text))
                    analyzed_count += 1
                    update_progress_bar(analyzed_count)

                sentiments = pd.Series(sentiments)

                sentiment_counts = sentiments.apply(lambda x: x[0]).value_counts()
                positive_count = sentiment_counts.get('POSITIVE', 0)
                negative_count = sentiment_counts.get('NEGATIVE', 0)
                neutral_count = sentiment_counts.get('NEUTRAL', 0)
                badword_count = sentiment_counts.get('BAD WORD', 0)

                overall_score = (positive_count / total_entries) * 100 if total_entries > 0 else 0

                output.clear_output()  # Clear loading text before displaying the results
                print(f"\nOverall Sentiment Score: {overall_score:.2f}%")
                display(HTML(df.to_html(classes='widget-box')))

                if sentiment_counts.get('BAD WORD', 0) > 0 or overall_score < 15:
                    overall_sentiment = "BAD WORD"
                elif 25 <= overall_score <= 50:
                    overall_sentiment = "NEUTRAL"
                else:
                    overall_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])[0]

                ai_response = generate_dynamic_response(overall_sentiment, overall_score)

                if overall_sentiment == "BAD WORD":
                    score_display = f'<div class="score-display badword-score">'
                else:
                    score_display = f'<div class="score-display {overall_sentiment.lower()}-score">'

                score_display += f'<div class="jump">Overall Sentiment Score: {overall_score:.2f}%</div>'
                score_display += f'<div class="jump">Overall Sentiment: {overall_sentiment}</div>'
                score_display += f'<div class="jump">AI Response: {ai_response}</div>'
                score_display += '</div>'

                display(HTML(score_display))

        upload.observe(on_file_upload, names='value')
        display(upload)

analyze_csv_button.on_click(on_analyze_csv_click)
display(analyze_csv_button, output)
