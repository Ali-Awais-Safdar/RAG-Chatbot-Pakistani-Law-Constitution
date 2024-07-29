import unicodedata
from langdetect import detect
from urduhack import normalize
from urduhack.urdu_characters import URDU_ALL_CHARACTERS

urdu_to_latin_map = {
    'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ٹ': 'tt', 'ث': 's', 'ج': 'j',
    'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ڈ': 'dd', 'ذ': 'z', 'ر': 'r',
    'ڑ': 'rr', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z',
    'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k',
    'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ں': 'n', 'و': 'w', 'ہ': 'h',
    'ء': "'", 'ی': 'y', 'ے': 'e', 'آ': 'aa', 'ؤ': 'o', 'ئ': 'y', 'ؐ': 'sa',
    ' ': ' ' 
}

latin_to_urdu_map = {v: k for k, v in urdu_to_latin_map.items()}

def urdu_to_latin(text):
    return ''.join(urdu_to_latin_map.get(char, char) for char in text)

def latin_to_urdu(text):
    return ''.join(latin_to_urdu_map.get(char, char) for char in text)

def process_urdu_text(text):
    text = unicodedata.normalize('NFKC', text)
    lang = detect(text)
    
    if lang == 'ur':
        text = normalize(text)
        
        text = ''.join([char if char in URDU_ALL_CHARACTERS else ' ' for char in text])
    
    return text, lang

def is_rtl(text):
    return ord(text[0]) >= 0x0600 and ord(text[0]) <= 0x06FF


sample_text = "حکومت خود مختار ہے"
processed_text, detected_lang = process_urdu_text(sample_text)
print(f"Processed text: {processed_text}")
print(f"Detected language: {detected_lang}")
print(f"Is RTL: {is_rtl(processed_text)}")

latin_text = urdu_to_latin(processed_text)
print(f"Latin transliteration: {latin_text}")

reverted_urdu_text = latin_to_urdu(latin_text)
print(f"Reverted Urdu text: {reverted_urdu_text}")