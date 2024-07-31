import pytesseract as pt
from PIL import Image

    
def ocr( image_path, lang='eng+urd'):
        img = Image.open(image_path)
        text = pt.image_to_string(img, lang=lang)
        confidence = pt.image_to_data(img, lang=lang, output_type=pt.Output.DICT)
        conf_avg = sum(int(x) for x in confidence['conf'] if x != '-1') / len(confidence['conf'])
        return text, conf_avg

