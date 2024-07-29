from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
import json
import os

# Text Normalization

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, '../data/legal_terms.json'), 'r') as f:
    legal_terms = json.load(f)

def normalize_legal_text(tokens):
    """
    Normalizes legal text tokens by performing several transformations:
    
    1. Matches and replaces custom legal terms.
    2. Corrects spelling of tokens.
    3. Lemmatizes tokens.
    4. Stems tokens.
    
    Args:
        tokens (list of str): The list of tokens to be normalized.
    
    Returns:
        list of str: The list of normalized tokens.
    """

    normalized_tokens = []
    i = 0
    while i < len(tokens):
        matched = False
        for term in legal_terms:
            term_tokens = term.split()
            # if the legal term itself is more than one word
            if tokens[i:i+len(term_tokens)] == term_tokens:
                replacement_tokens = legal_terms[term.lower()].split()
                normalized_tokens.extend(replacement_tokens)
                i += len(term_tokens)
                matched = True
                break
        if not matched:
            corrected_token = str(TextBlob(tokens[i]).correct())
            lemma = lemmatizer.lemmatize(corrected_token.lower())
            stem = stemmer.stem(lemma)
            normalized_tokens.append(stem)
            i += 1

    return normalized_tokens
