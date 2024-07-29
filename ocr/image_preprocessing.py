import cv2
import numpy as np
from deskew import determine_skew
import pytesseract

def preprocess_image(image_path):
    """
    Preprocesses the image for OCR by performing several steps including:
    - Reading the image from the specified path.
    - Converting the image to grayscale.
    - Applying binary thresholding to binarize the image.
    - Correcting skew by rotating the image.
    - Reducing noise using Non-Local Means Denoising.
    - Sharpening the image using a sharpening kernel.

    Args:
        image_path (str): The path to the image file to be preprocessed.

    Returns:
        numpy.ndarray: The preprocessed image ready for OCR.
    """
    # Read image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarization
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Skew correction
    angle = determine_skew(binary)
    rotated = rotate_image(binary, angle)

    # Noise reduction
    denoised = cv2.fastNlMeansDenoising(rotated, h=30)

    # Sharpening
    kernel = np.array([[-1, -1, -1], 
                       [-1,  9, -1], 
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    return sharpened

def rotate_image(image, angle):
    """
    Rotates the image by the specified angle.

    Args:
        image (numpy.ndarray): The image to be rotated.
        angle (float): The angle by which the image should be rotated.

    Returns:
        numpy.ndarray: The rotated image.
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def perform_ocr(image):
    """
    Performs Optical Character Recognition (OCR) on the given image using Tesseract.

    Args:
        image (numpy.ndarray): The image on which OCR is to be performed.

    Returns:
        str: The text extracted from the image by OCR.
    """
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)
    return text

# Example usage
image_path = r'C:\Users\PMLS\Desktop\RAG\sample.jpg'
preprocessed_image = preprocess_image(image_path)
cv2.imwrite(r'C:\Users\PMLS\Desktop\RAG\preprocessed_sample.jpg', preprocessed_image)

# Perform OCR
text = perform_ocr(preprocessed_image)
print("OCR Result:")
print(text)
