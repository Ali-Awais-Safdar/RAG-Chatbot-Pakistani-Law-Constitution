import cv2
from text_processing import preprocess_image, perform_ocr

# Example usage
image_path = r'C:\Users\PMLS\Desktop\RAG\sample.jpg'
preprocessed_image = preprocess_image(image_path)
cv2.imwrite(r'C:\Users\PMLS\Desktop\RAG\preprocessed_sample.jpg', preprocessed_image)

# Perform OCR
text = perform_ocr(preprocessed_image)
print("OCR Result:")
print(text)
