from text_processing.cleaning import clean_legal_text
from text_processing.normalization import normalize_legal_text
from text_processing.pattern_matching import extract_patterns
from text_processing.tokenization import tokenize_legal_text
import unittest

class TestCleanLegalText(unittest.TestCase):
    
    def test_normalize_whitespace(self):
        sample_text = "This   is   a   test."
        expected_result = "is test"
        self.assertEqual(clean_legal_text(sample_text), expected_result)
    
    def test_complex_text(self):
        sample_text = ("135. Abetment WAPDA of desertion of soldier, sailor [or] [airman.] ")
        expected_result = ("abetment Water and Power Development Authority desertion soldier sailor or airman")
        self.assertEqual(clean_legal_text(sample_text), expected_result)

    def test_more_complex_text(self):
        sample_text = ("By A.O., the Govt. or govt. has decided to include WAPDA and PC for max or max. profit p/a. ")
        expected_result = ("by Administrative Order government or government decided include Water and Power Development Authority and Privatization Commission maximum or maximum profit per annum")
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
        expected_result = "is test"
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
        self.assertEqual(normalize_legal_text(tokens), expected_output)
        
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
        
    def test_sentences_with_citations(self):
        text = "Sec.1.2 The court finds that the defendant Mr Smith violated Sec.3(a)-2 of the Act. The court orders the defendant to pay a fine of 100."
        expected_output = [["Sec.1.2", "The", "court", "finds", "that", "the", "defendant", "Mr", "Smith", "violated", "Sec.3(a)-2", "of", "the", "Act", "."], ["The", "court", "orders", "the", "defendant", "to", "pay", "a", "fine", "of", "100", "."]]
        self.assertEqual(tokenize_legal_text(text), expected_output)

    def test_sentences_with_citations_2(self):
        text = "Sec. 1.2 Art. 184(3) the Ordinance 784 court also sec. 6.8 Sec. 1.2 finds Art. 9 hiding act 67. Sec.3.5 Sec.6(8)-d defendant 114 Stat. 899 mr smith violated Sec. 3(a)-2 act. Art. 184(3) on Pg. 45 also Sec. 4.66 constitution PPC 4444 important. Sec. 4 and Pakistan Penal Code 1860 implies that Companies Ordinance 1984 often referenced refers to PLD 2020 SC 1 case law Rule 5(10). SRO 123(I)/2020 is also relevant. 18th Amendment brought significant changes. Presidential Order No. 1 of 1977 issued 3rd Amendment also cool refer Notification No. 1234-G/2020 Anti-Terrorism Act 1997 Review Petition No. 567/2020 filed check 2019 clc 123 relevant high court cases Income Tax Ordinance 2001 also cited 144 Stat. 789 also states thing AIR 1990 SC 123 important precedent Constitution Petition No. 45/2021. ECP Order No. 123/2019 notable Companies Ord 1984 also checkeddefinition queen omitted A.O., 1961 Art. 2 and school (w.e.f. the 23rd March, 1956) case smith volume jones 123 f2d 456 2022 court interpreted Section 123(a) act hearing date set aug 15 2024 adultery report offences zina enforcement hudood Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979) workmens breach contract repealing Act, 1925 (III of 1925), s. 2 school"
        expected_output = [['Sec. 1.2', 'Art. 184(3)', 'the', 'Ordinance 784', 'court', 'also', 'sec. 6.8', 'Sec. 1.2', 'finds', 'Art. 9', 'hiding', 'act 67', '.'], ['Sec.3.5', 'Sec.6(8)-d', 'defendant', '114 Stat. 899', 'mr', 'smith', 'violated', 'Sec. 3(a)-2', 'act', '.'], ['Art. 184(3)', 'on', 'Pg. 45', 'also', 'Sec. 4.66', 'constitution', 'PPC 4444', 'important', '.'], ['Sec. 4', 'and', 'Pakistan Penal Code 1860', 'implies', 'that', 'Companies Ordinance 1984', 'often', 'referenced', 'refers', 'to', 'PLD 2020 SC 1', 'case', 'law', 'Rule 5(10)', '.'], ['SRO 123(I)/2020', 'is', 'also', 'relevant', '.'], ['18th Amendment', 'brought', 'significant', 'changes', '.'], ['Presidential Order No. 1 of 1977', 'issued', '3rd Amendment', 'also', 'cool', 'refer', 'Notification No. 1234-G/2020', 'Anti-Terrorism Act 1997', 'Review Petition No. 567/2020', 'filed', 'check', '2019', 'clc', '123', 'relevant', 'high', 'court', 'cases', 'Income Tax Ordinance 2001', 'also', 'cited', '144 Stat. 789', 'also', 'states', 'thing', 'AIR 1990 SC 123', 'important', 'precedent', 'Constitution Petition No. 45/2021', '.'], ['ECP Order No. 123/2019', 'notable', 'Companies Ord 1984', 'also', 'checkeddefinition', 'queen', 'omitted', 'A.O., 1961', 'Art. 2', 'and', 'school', '(w.e.f. the 23rd March, 1956)', 'case', 'smith', 'volume', 'jones', '123', 'f2d', '456', '2022', 'court', 'interpreted', 'Section 123(a)', 'act', 'hearing', 'date', 'set', 'aug', '15', '2024', 'adultery', 'report', 'offences', 'zina', 'enforcement', 'hudood', 'Ordinance, 1979 (VII of 1979), s. 19', '(w.e.f the 10th day of February, 1979)', 'workmens', 'breach', 'contract', 'repealing', 'Act, 1925 (III of 1925), s. 2', 'school']]
        self.assertEqual(tokenize_legal_text(text), expected_output)



