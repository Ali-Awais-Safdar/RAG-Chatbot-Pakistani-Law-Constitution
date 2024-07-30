import unittest
from ocr import post_correction_ocr

class TestPostCorrectionOCR(unittest.TestCase):
    
    def setUp(self):
        self.legal_dict = ["this", "is", "a", "test", "soldier", "sailor", "airman", "desertion", "abetment"]

    def test_basic_spell_correction(self):
        text = "Ths is a tst"
        expected = "this is a test"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_correctly_spelled_words(self):
        text = "This is a test"
        expected = "This is a test"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_mixed_spelling_and_numerical_format(self):
        text = "Ths is a tst 1f 2"
        expected = "this is a test 1F.2"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_no_matches_in_legal_dictionary(self):
        text = "qwerty asdfgh"
        expected = "qwerty asdfgh"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_close_match_in_legal_dictionary(self):
        text = "Ths is a tets"
        expected = "this is a test"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_empty_input(self):
        text = ""
        expected = ""
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_only_numbers(self):
        text = "123 456"
        expected = "123 456"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_special_characters(self):
        text = "Hello, World! @2024 & #Python"
        expected = "hello world 2024 python"
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

    def test_complex_text(self):
        text = "135. Abetment WAPDA of desertion of soldier, sailor [or] [airman.]"
        expected = "135. abetment WAPDA of desertion of soldier sailor or airman."
        result = post_correction_ocr(text, self.legal_dict)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
