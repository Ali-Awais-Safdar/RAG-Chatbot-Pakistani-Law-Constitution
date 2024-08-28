from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
from utils import get_citation_pattern
import json
import os

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
    5. Preserve citations/dates
    
    Args:
        tokens (list of str): The list of tokens to be normalized.
    
    Returns:
        list of str: The list of normalized tokens.
    """
    if not isinstance(tokens, list):
        raise TypeError("tokens must be a list")
    # return empty string if text is empty
    if not tokens:
        return []
    # ensure legal_abbreviations is a dictionary
    if not isinstance(legal_terms, dict):
        raise TypeError("legal_terms must be a dictionary")
    
    citation_pattern = get_citation_pattern()
    placeholders = {}
    normalized_tokens = []
    i = 0
    citation_index = 0
    final_tokens = []

    while i < len(tokens):
        token = tokens[i]
        if citation_pattern.match(token):
            placeholder = f"__CITATION_{citation_index}__"
            placeholders[placeholder] = token
            normalized_tokens.append(placeholder)
            citation_index += 1
        else:
            normalized_tokens.append(token)
        i += 1

    i = 0
    final_tokens = []
    while i < len(normalized_tokens):
        token = normalized_tokens[i]
        if token in placeholders:
            final_tokens.append(token)
            i += 1
            continue

        matched = False
        for term in legal_terms:
            term_tokens = term.split()
            if normalized_tokens[i:i+len(term_tokens)] == term_tokens:
                replacement_tokens = legal_terms[term.lower()].split()
                final_tokens.extend(replacement_tokens)
                i += len(term_tokens)
                matched = True
                break

        if not matched:
            corrected_token = str(TextBlob(token).correct())
            lemma = lemmatizer.lemmatize(corrected_token.lower())
            stem = stemmer.stem(lemma)
            final_tokens.append(stem)
            i += 1

    final_tokens = [placeholders.get(token, token) for token in final_tokens]

    return final_tokens

# tokens = ["Sec. 1.2", "court", "finds", "Sec.3.5", "defendant", "mr", "smith", "violated", "Sec. 3(a)-2", "Act", "according", "Ordinance 1444", "far", "more", "crimes", "than", "Sec. 3(a)-12", "acts"]
# print("\nInput:\t" + str(tokens) + "\nOutput:\t" + str(normalize_legal_text(tokens)))
