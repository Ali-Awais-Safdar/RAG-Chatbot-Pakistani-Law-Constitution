import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer

# Load custom legal stopwords and abbreviations
with open('legal_stopwords.json', 'r') as f:
    legal_stopwords = set(json.load(f))

with open('legal_abbreviations.json', 'r') as f:
    legal_abbreviations = json.load(f)

# Example usage
tokenized = tokenize_legal_text(cleaned_text)
print(tokenized)
