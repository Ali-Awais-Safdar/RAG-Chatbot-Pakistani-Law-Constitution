import cv2
#from text_processing import preprocess_image, perform_ocr
import unittest
from tests.test_text_processing import TestTokenizeLegalText, TestCleanLegalText, TestNormalizeLegalText, TestPatternExtraction
from text_processing import clean_legal_text
from ml_integration.legal_qa_system import legal_qa_system, load_legal_documents, load_model

# Example usage
# image_path = r'C:\Users\PMLS\Desktop\RAG\sample.jpg'
# preprocessed_image = preprocess_image(image_path)
# cv2.imwrite(r'C:\Users\PMLS\Desktop\RAG\preprocessed_sample.jpg', preprocessed_image)

# # Perform OCR
# text = perform_ocr(preprocessed_image)
# print("OCR Result:")
# print(text)

# # Run tests
# unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCleanLegalText))
# unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestNormalizeLegalText))
# unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestTokenizeLegalText))

question = """What is the penalty for copyright infringement?"""
documents = load_legal_documents() # Implement this function to load your legal corpus
fine_tuned_model, tokenizer = load_model()
if documents and isinstance(documents, list):
  cleaned_documents = []
  for i in range(len(documents)):
    cleaned_documents.append(clean_legal_text(documents[i]))
  print(cleaned_documents)
  answer = legal_qa_system(question, cleaned_documents, fine_tuned_model, tokenizer)
  print(f"\nQuestion: {question}")
  print(f"Answer: {answer}")
else:
  print("Wrong Documents")

