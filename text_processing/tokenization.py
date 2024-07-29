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

def clean_legal_text(text):
    # Remove special characters, keeping legally relevant symbols
    text = re.sub(r'[^\w\s\.,;\:\-\(\)]', '', text)
    
    # Expand abbreviations first to avoid case issues
    for abbr, expansion in legal_abbreviations.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', expansion, text, flags=re.IGNORECASE)
    
    # Convert to lowercase, preserving specific legal terms
    text = ' '.join([word if word in legal_abbreviations.values() else word.lower() for word in text.split()])
    
    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in legal_stopwords]
    text = ' '.join(words)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Example usage
sample_text = "Sec. 1.2 The court finds that the defendant, Mr. Smith, violated Sec. 3(a)-2 of the Act."
cleaned_text = clean_legal_text(sample_text)
print(cleaned_text)


def tokenize_legal_text(text):
    # Simplified sentence splitting based on common punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
   # print("Sentences after split:", sentences)  # Debugging statement

    # Custom word tokenizer pattern
    word_tokenizer = RegexpTokenizer(r'\w+(?:-\w+)*|\d+(?:\.\d+)?%?|\w+\.\w+|\S+')
    
    tokenized_text = []
    for sentence in sentences:
        words = word_tokenizer.tokenize(sentence)
    #    print("Words in sentence:", words)  # Debugging statement
        tokenized_text.append(words)
    
    return tokenized_text

# Example usage
tokenized = tokenize_legal_text(cleaned_text)
print(tokenized)
