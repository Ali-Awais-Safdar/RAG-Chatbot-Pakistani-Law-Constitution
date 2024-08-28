import json
import re
import os
from utils.helpers import get_citation_pattern

# load custom legal stopwords and abbreviations
current_dir = os.path.dirname(__file__)
with open(os.path.join(current_dir, "../data/legal_abbreviations.json"), "r") as f:
    legal_abbreviations = json.load(f)
with open(os.path.join(current_dir, "../data/legal_stopwords.json"), "r") as f:
    legal_stopwords = json.load(f)

def clean_legal_text(text):
    """
    Cleans and normalizes legal text by performing several transformations:
    
    1. Normalizes case while preserving specific terms.
    2. Removes stopwords.
    3. Expands legal abbreviations.
    4. Removes leading numbers, underscores and periods.
    5. Removes punctuation.
    6. Normalizes whitespace.
    7. Preserve citaions/dates
    
    Args:
        text (str): The legal text to be cleaned.
    
    Returns:
        str: The cleaned and normalized legal text.
    """

    # ensure text is a string 
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # return empty string if text is empty
    if not text:
        return ""
    # ensure legal_abbreviations is a dictionary
    if not isinstance(legal_abbreviations, dict):
        raise TypeError("legal_abbreviations must be a dictionary")
    # ensure legal_stopwords is a list
    if not isinstance(legal_stopwords, list):
        raise TypeError("legal_stopwords must be a set")

    # removing page number text
    text = re.sub(r"[pP][aA][gG][eE]\s*\d+[oO][fF]\d+", "", text) # comment out if page numbers are needed

    # identifying and replacing citations with placeholders
    citation_pattern = get_citation_pattern()
    citations = citation_pattern.findall(text)
    citations = ["".join(citation) for citation in citations]
    # print("\nCITATIONS:\t" + str((citations)))
    # print("\nCITATIONS LEN:\t" + str(len((citations))))
    placeholders = {f"__citation_{i}__": citation for i, citation in enumerate(citations)}
    for placeholder, citation in placeholders.items():
        text = text.replace(citation, placeholder)
    
    # normalizing case and preserve specific terms
    text = " ".join([word if word in legal_abbreviations else word.lower() for word in text.split()])

    # removing stopwords
    words = [word for word in text.split() if word not in legal_stopwords]
    text = " ".join(words)  

    # expanding the abbreviations 
    for abbr, expansion in legal_abbreviations.items():
        escaped_abbr = re.escape(abbr)
        pattern = r"(\W|^)" + escaped_abbr + r"(?=\s|\Z|\W(?!\w))"
        replacement = r"\1" + expansion
        text = re.sub(pattern, replacement, text)
        
    # removing leading numbers and periods
    text = re.sub(r"\d+\.\s*", "", text)

    # removing punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # preserving the citations by replacing the placeholders
    for placeholder, citation in placeholders.items():
        text = text.replace(placeholder, citation)

    # remove underscores
    text = re.sub(r"\b_\b", "", text)

    # normalizing whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
