import json
import re

# Text Cleaning

# load custom legal stopwords and abbreviations
with open('legal_stopwords.json', 'r') as f:
    legal_stopwords = set(json.load(f))

with open('legal_abbreviations.json', 'r') as f:
    legal_abbreviations = json.load(f)

def clean_legal_text(text):
    """
    Cleans and normalizes legal text by performing several transformations:
    
    1. Normalizes case while preserving specific terms.
    2. Removes stopwords.
    3. Expands legal abbreviations.
    4. Removes leading numbers, underscores and periods.
    5. Removes punctuation.
    6. Normalizes whitespace.
    
    Args:
        text (str): The legal text to be cleaned.
    
    Returns:
        str: The cleaned and normalized legal text.
    """

    # removing underscores otherwise theyre not handled
    text = text.replace('_', ' ')
    
    # normalizing case and preserve specific terms
    text = ' '.join([word if word in legal_abbreviations else word.lower() for word in text.split()])

    # removing stopwords
    words = text.split()
    words = [word for word in words if word not in legal_stopwords]
    text = ' '.join(words)  

    # expanding the abbreviations 
    for abbr, expansion in legal_abbreviations.items():
        escaped_abbr = re.escape(abbr)
        pattern = r'(\W|^)' + escaped_abbr + r'(?=\s|\Z|\W(?!\w))'
        replacement = r'\1' + expansion
        text = re.sub(pattern, replacement, text)
        
    # removing leading numbers and periods
    text = re.sub(r'^\d+\.\s*', '', text)

    # removing punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # normalizing whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
