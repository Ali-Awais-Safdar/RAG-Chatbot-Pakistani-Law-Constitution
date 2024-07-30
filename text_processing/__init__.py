"""
LegalTextProcessor is a package for processing legal text.

Modules:
- cleaning: Contains functions to clean legal text.
- normalization: Contains functions to normalize legal text.
- tokenization: Contains functions to tokenize legal text.
- pattern matching: Contains function to extract patterns from legal text.

Functions:
- clean_legal_text: Function to clean legal text.
- normalize_legal_text: Function to normalize legal text.
- tokenize_legal_text: Function to tokenize legal text.
- extract_patterns: Function to extract predefined legal patterns from legal text.
Version:
1.0.0
"""

from .cleaning import clean_legal_text
from .normalization import normalize_legal_text
from .tokenization import tokenize_legal_text
from .pattern_matching import extract_patterns

__all__ = ['clean_legal_text', 'normalize_legal_text', 'tokenize_legal_text','extract_patterns']

__version__ = '1.0.0'
