import pytesseract as pt
from PIL import Image

class OCR:
    def __init__(self, image_path, legal_dictionary_path):
        self.image_path = image_path
        self.legal_dictionary_path = legal_dictionary_path

    def ocr(self, image_path, lang='eng+urd'):
        img = Image.open(image_path)
        text = pt.image_to_string(img, lang=lang)
        confidence = pt.image_to_data(img, lang=lang, output_type=pt.Output.DICT)
        conf_avg = sum(int(x) for x in confidence['conf'] if x != '-1') / len(confidence['conf'])
        return text, conf_avg

if __name__ == "__main__":
    import os

    os.chdir("/mnt/c/Users/muhammad.hadi/Downloads")
    pt.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    
    image_path = input('Enter Image Path: ')
    legal_dictionary_path = input('Enter Legal Dictionary Path: ')

    ocr_instance = OCR(image_path, legal_dictionary_path)
    text, confidence = ocr_instance.ocr(image_path)
    print(f"Extracted Text: {text}")
    print(f"Confidence: {confidence}")
