from text_processing.cleaning import clean_legal_text
from text_processing.normalization import normalize_legal_text
from text_processing.pattern_matching import extract_patterns
from text_processing.tokenization import tokenize_legal_text
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

    def test_more_complex_text(self):
        sample_text = ("By A.O., the Govt. or govt. has decided to include WAPDA and PC for max or max. profit p/a. ")
        expected_result = ("Administrative Order government government decided include Water and Power Development Authority Privatization Commission maximum maximum profit per annum")
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
    
    def test_sentences_with_citations(self):
        text = "Sec.1.2 The court finds that the defendant Mr. Smith violated Sec.3(a)-2 of the Act."
        expected_output = "Sec.1.2 court finds defendant mr smith violated Sec.3(a)-2 act"
        self.assertEqual(clean_legal_text(text), expected_output)

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

class TestTokenizeLegalText(unittest.TestCase):
    
    def test_simple_sentence(self):
        text = "The court is in session."
        expected_output = [["The", "court", "is", "in", "session", "."]]
        self.assertEqual(tokenize_legal_text(text), expected_output)
    
    def test_sentence_with_abbreviations(self):
        text = "The US Supreme Court ruled in favor."
        expected_output = [["The", "US", "Supreme", "Court", "ruled", "in", "favor", "."]]
        self.assertEqual(tokenize_legal_text(text), expected_output)
    
    def test_sentence_with_numbers(self):
        text = "The court imposed a fine of Rs 100."
        expected_output = [["The", "court", "imposed", "a", "fine", "of", "Rs", "100", "."]]
        self.assertEqual(tokenize_legal_text(text), expected_output)

    def test_empty_input(self):
        text = ""
        expected_output = [[]]
        self.assertEqual(tokenize_legal_text(text), expected_output)

    def test_sentence_with_legal_terms(self):
        text = "The plaintiff filed a motion for summary judgment"
        expected_output = [["The", "plaintiff", "filed", "a", "motion", "for", "summary", "judgment"]]
        self.assertEqual(tokenize_legal_text(text), expected_output)

    # def test_sentence_with_citations(self):
    #     text = "See Roe v. Wade, 410 U.S. 113 (1973)."
    #     expected_output = [["See", "Roe", "v.", "Wade", ",", "410", "U.S.", "113", "(", "1973", ")", "."]]
    #     self.assertEqual(tokenize_legal_text(text), expected_output)
        
    # def test_sentences_with_citations(self):
    #     text = "Sec.1.2 The court finds that the defendant Mr Smith violated Sec.3(a)-2 of the Act. The court orders the defendant to pay a fine of 100."
    #     expected_output = [["Sec.1.2", "The", "court", "finds", "that", "the", "defendant", "Mr", "Smith", "violated", "Sec.3(a)-2", "of", "the", "Act", "."], ["The", "court", "orders", "the", "defendant", "to", "pay", "a", "fine", "of", "100", "."]]
    #     self.assertEqual(tokenize_legal_text(text), expected_output)


