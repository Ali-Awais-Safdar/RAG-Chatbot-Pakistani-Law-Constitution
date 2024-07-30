import unittest
import cv2
import numpy as np
from my_package import preprocess_image, rotate_image, perform_ocr

class TestMyPackage(unittest.TestCase):

    def setUp(self):
        # This method will run before each test case
        self.image_path = r'C:\Users\PMLS\Desktop\RAG\sample.jpg'
        self.image = cv2.imread(self.image_path)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
    def test_preprocess_image(self):
        preprocessed_image = preprocess_image(self.image_path)
        self.assertIsInstance(preprocessed_image, np.ndarray)
        self.assertEqual(preprocessed_image.shape, self.gray_image.shape)
        
    def test_rotate_image(self):
        angle = 45
        rotated_image = rotate_image(self.gray_image, angle)
        self.assertIsInstance(rotated_image, np.ndarray)
        self.assertEqual(rotated_image.shape, self.gray_image.shape)
        
    def test_perform_ocr(self):
        preprocessed_image = preprocess_image(self.image_path)
        text = perform_ocr(preprocessed_image)
        self.assertIsInstance(text, str)

if __name__ == '__main__':
    unittest.main()
