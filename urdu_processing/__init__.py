
"""
Urdu Text Processing Module

This module provides functions for handling Urdu Unicode text, including
normalization, language detection, RTL text handling, and transliteration
between Urdu and Latin scripts.

Functions:
- process_urdu_text: Processes and normalizes Urdu text.
- is_rtl: Checks if the given text is written in a right-to-left script.
- urdu_to_latin: Transliterates Urdu text to Latin script.
- latin_to_urdu: Transliterates Latin script to Urdu text.
"""

from .unicode_handler import process_urdu_text, is_rtl, urdu_to_latin, latin_to_urdu

__all__ = ['process_urdu_text', 'is_rtl', 'urdu_to_latin', 'latin_to_urdu']
