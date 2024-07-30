import re
from difflib import get_close_matches
from spellchecker import SpellChecker

spell = SpellChecker()

def load_legal_dictionary(dictionary_path):
    with open(dictionary_path, 'r') as file:
        legal_dict = file.read().splitlines()
    return legal_dict

def post_correction_ocr(text, legal_dict):
    words = text.split()
    corrected_words = []

    for word in words:
        if word in legal_dict:
            corrected_words.append(word)
        else:
            correction = spell.correction(word)
            if correction != word:
                legal_matches = get_close_matches(word, legal_dict, n=1, cutoff=0.8)
                if legal_matches:
                    correction = legal_matches[0]
                else:
                    correction = word  
            corrected_words.append(correction)

    corrected_text = ' '.join(corrected_words)
    corrected_text = re.sub(r'(\d+)\s*[F|f]\s*(\d+)', r'\1F.\2', corrected_text)
    return corrected_text

if __name__ == "__main__":
    legal_dictionary_path = input('Enter Legal Dictionary Path: ')
    text = input('Enter OCR Text: ')

    legal_dict = load_legal_dictionary(legal_dictionary_path)
    corrected_text = post_correction_ocr(text, legal_dict)
    print(f"Corrected Text: {corrected_text}")
