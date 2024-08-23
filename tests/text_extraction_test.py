import unittest
from ocr import text_extraction

class TestTextExtraction(unittest.TestCase):

    def test_simple_image(self):
        image_path = '/home/hadi/RAG-Chatbot-Pakistani-Law-Constitution/Images_OCR/image_photo.jpeg'
        expected_text = 'Hello Checking if OCR is functioning.'
        text, conf_avg = text_extraction(image_path, lang='eng')
        self.assertIn(expected_text, text)
        self.assertGreater(conf_avg, 90)

    def test_noisy_image(self):
        image_path = 'tests/images/noisy_text.png'
        expected_text = 'This is a noisy text.'
        text, conf_avg = text_extraction(image_path, lang='eng')
        self.assertIn(expected_text, text)
        self.assertGreater(conf_avg, 50)  # Assuming noisy image will have lower confidence

    def test_blank_image(self):
        image_path = 'tests/images/blank_image.png'
        expected_text = ''
        text, conf_avg = text_extraction(image_path, lang='eng')
        self.assertEqual(text.strip(), expected_text)
        self.assertEqual(conf_avg, 0)

    def test_multilingual_image(self):
        image_path = 'tests/images/multilingual_text.png'
        expected_text_eng = 'This is English text.'
        expected_text_urd = 'یہ اردو کا متن ہے۔'
        text, conf_avg = text_extraction(image_path, lang='eng+urd')
        self.assertIn(expected_text_eng, text)
        self.assertIn(expected_text_urd, text)
        self.assertGreater(conf_avg, 70)  # Assuming average confidence for multilingual text

if __name__ == '__main__':
    unittest.main()
