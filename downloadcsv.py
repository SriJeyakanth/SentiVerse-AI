from google.colab import files
uploaded = files.upload()
import pandas as pd

# Access the CSV files
positive_words = pd.read_csv('positive.csv')
negative_words = pd.read_csv('negative.csv')
tamil_words = pd.read_csv('tamilbw.csv')
