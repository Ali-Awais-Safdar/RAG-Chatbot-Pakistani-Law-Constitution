import unittest
from urdu_processing.unicode_handler import process_urdu_text, is_rtl, urdu_to_latin, latin_to_urdu

class TestUrduTextProcessing(unittest.TestCase):

    def test_unicode_normalization(self):
        sample_text = "یہ ایک مثال ہے"
        expected_output = "یہ ایک مثال ہے"
        processed_text, _ = process_urdu_text(sample_text)
        self.assertEqual(processed_text, expected_output)
    
    def test_language_detection(self):
        urdu_text = "یہ ایک مثال ہے"
        english_text = "This is an example."
        mixed_text = "یہ ایک مثال ہے This is an example."
        
        _, lang_urdu = process_urdu_text(urdu_text)
        _, lang_english = process_urdu_text(english_text)
        _, lang_mixed = process_urdu_text(mixed_text)
        
        self.assertEqual(lang_urdu, 'ur')
        self.assertEqual(lang_english, 'en')
        self.assertEqual(lang_mixed, 'ur')  # Depending on the majority or first detected language
    
    def test_rtl_detection(self):
        urdu_text = "یہ ایک مثال ہے"
        english_text = "This is an example."
        
        self.assertTrue(is_rtl(urdu_text))
        self.assertFalse(is_rtl(english_text))
    
    def test_mixed_language_handling(self):
        mixed_text = "یہ ایک مثال ہے This is an example."
        processed_text, _ = process_urdu_text(mixed_text)
        self.assertIn("یہ ایک مثال ہے", processed_text)
        self.assertIn("This is an example.", processed_text)
    
    def test_urdu_to_latin(self):
        urdu_text = "حکومت خود مختار ہے"
        expected_latin = "hkumt khud mkhtar h"
        self.assertEqual(urdu_to_latin(urdu_text), expected_latin)
    
    def test_latin_to_urdu(self):
        latin_text = "hkumt khud mkhtar h"
        expected_urdu = "حکومت خود مختار ہے"
        self.assertEqual(latin_to_urdu(latin_text), expected_urdu)

