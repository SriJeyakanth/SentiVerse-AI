from flask import Flask, request, jsonify
from transformers import pipeline
import pandas as pd

app = Flask(__name__)
nlp = pipeline('sentiment-analysis')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json['text']
    result = nlp(text)
    score = result[0]['score'] * 100  # Convert to a scale of 100
    label = result[0]['label']
    comment = generate_comment(label, score)
    return jsonify({'score': score, 'label': label, 'comment': comment})

def generate_comment(label, score):
    if label == 'POSITIVE':
        return f"Great! This feedback has a positive sentiment with a score of {score:.2f}."
    else:
        return f"There's some negativity with a score of {score:.2f}. Consider addressing the concerns."

@app.route('/analyze_csv', methods=['POST'])
def analyze_csv():
    file = request.files['file']
    df = pd.read_csv(file)
    results = []
    for text in df['feedback']:
        result = nlp(text)[0]
        score = result['score'] * 100
        label = result['label']
        comment = generate_comment(label, score)
        results.append({'text': text, 'score': score, 'label': label, 'comment': comment})
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 
