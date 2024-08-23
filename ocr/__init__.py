"""
MyPackage is a package for image preprocessing and optical character recognition (OCR).

Modules:
- pre_processing: Contains functions for image preprocessing and OCR.

Version:
1.0.0
"""



from .image_preprocessing import preprocess_image
from .ocr_postprocessing import postprocess_text
from .text_extraction import text_extraction

__all__ = ['preprocess_image', 'postprocess_text', 'text_extraction']
