from text_processing.cleaning import clean_legal_text
from text_processing.normalization import normalize_legal_text
from pattern_matching import extract_patterns
import unittest

class TestCleanLegalText(unittest.TestCase):
    
    def test_normalize_whitespace(self):
        sample_text = "This   is   a   test."
        expected_result = "test"
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_normalize_whitespace(self):
        sample_text = "This   is   a   test."
        expected_result = "test"
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_complex_text(self):
        sample_text = ("135. Abetment WAPDA of desertion of soldier, sailor [or] [airman.] ")
        expected_result = ("abetment Water and Power Development Authority desertion soldier sailor or airman")
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_empty_string(self):
        sample_text = ""
        expected_result = ""
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_only_whitespace(self):
        sample_text = "     "
        expected_result = ""
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_mixed_whitespace(self):
        sample_text = "This\tis\na test."
        expected_result = "test"
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_special_characters(self):
        sample_text = "Hello, World! @2024 & #Python"
        expected_result = "hello world 2024 python"
        self.assertEqual(clean_legal_text(sample_text), expected_result)

class TestNormalizeLegalText(unittest.TestCase):

    def test_normalize_legal_text_with_legal_terms(self):
        # Test with tokens that do not include legal terms
        tokens = ["The", "courts", "finding", "overruled", "previous", "judgment"]
        expected_output = ["the", "court", "find", "rejected", "prior", "judgement"]
        
        
    def test_normalize_legal_text_with_legal_term_2(self):
        # Test with tokens that do not include legal terms
        tokens = ["their", "findings", "are", "overruled"]
        expected_output = ["their", "find", "are", "rejected"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)

    def test_normalize_legal_text_without_legal_term(self):
        # Test with tokens that do NOT include legal terms
        tokens = ["this", "is", "a", "simple", "test", "sentence"]
        expected_output = ["this", "is", "a", "simple", "test", "sentenc"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)

    def test_normalize_legal_text_empty_input(self):
        # Test with empty input
        tokens = []
        expected_output = []
        self.assertEqual(normalize_legal_text(tokens), expected_output)

    def test_normalize_legal_text_multiple_legal_terms(self):
        # Test with multiple legal terms
        tokens = ["mitigating", "circumstances", "plea", "bargain", "statute", "of", "limitations"]
        expected_output = ["lessen", "factor", "deal", "time", "limit"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)

    def test_normalize_legal_text_mixed_tokens(self):
        # Test with mixed tokens
        tokens = ["The", "prosecutor", "presented", "the", "testimony"]
        expected_output = ["the", "state", "lawyer", "present", "the", "evidence"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)

    def test_normalize_legal_text_mixed_tokens_2(self):
        # Test with mixed tokens
        tokens = ["The", "statute", "of", "capital", "punishment", "statute", "of", "limitations"]
        expected_output = ["the", "law", "of", "death", "penalty", "time", "limit"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)
        
    def test_normalize_legal_text_unknown_terms(self):
        # Test with unknown terms
        tokens = ["unknown", "terms", "should", "be", "lemmatized", "and", "stemmed"]
        expected_output = ["unknown", "term", "should", "be", "lemmat", "and", "stem"]
        self.assertEqual(normalize_legal_text(tokens), expected_output)

class TestPatternExtraction(unittest.TestCase):

    def test_case_citations(self):
        text = "In the case of Smith v. Jones, 123 F.2d 456 (2022)."
        result = extract_patterns(text)
        self.assertEqual(result["case_citations"], ["Smith v. Jones, 123 F.2d 456 (2022)"])

    def test_statute_references(self):
        text = "Refer to 123 U.S.C. § 456 for details."
        result = extract_patterns(text)
        self.assertEqual(result["statute_references"], ["123 U.S.C. § 456"])

    def test_dates(self):
        text = "The hearing date was set for Aug 15, 2024."
        result = extract_patterns(text)
        self.assertEqual(result["dates"], ["Aug 15, 2024"])

    def test_acts_references(self):
        text = "This is defined in the Act, 1979."
        result = extract_patterns(text)
        self.assertEqual(result["acts_references"], ["Act, 1979"])

    def test_sections(self):
        text = "Refer to Section 123(a) for more information."
        result = extract_patterns(text)
        self.assertEqual(result["sections"], ["Section 123(a)"])

    def test_repealed_statements(self):
        text = "[Adultery.] Rep. by the Offences of Zina (Enforcement of Hudood) Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979)."
        result = extract_patterns(text)
        self.assertEqual(result["repealed_statements"], ["Rep. by the Offences of Zina (Enforcement of Hudood) Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979)"])

