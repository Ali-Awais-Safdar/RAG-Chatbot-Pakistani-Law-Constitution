import re

def extract_patterns(text):
    patterns = {
        "case_citations": r"\b[A-Za-z]+ v\. [A-Za-z]+, \d+ [A-Z]\.[A-Za-z]* \d+ \(\d{4}\)\b",
        "statute_references": r"\d+ U\.S\.C\. § \d+[a-z]?",
        "dates": r"\b(?:w\.e\.f\. )?\d{1,2}(?:st|nd|rd|th)? (?:day of )?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),? \d{4}\b",
        "acts_references": r"\b(?:Act|Ordinance),? \d{4}\b",
        "sections": r"\b[sS]ection \d+[a-zA-Z]?\b",
        "repealed_statements": r"\bRep\. by the [A-Za-z0-9() ]+ Ordinance, \d{4} \([A-Z]+ of \d{4}\), s\. \d+ \((?:w\.e\.f\. )?\d{1,2}(?:st|nd|rd|th)? (?:day of )?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),? \d{4}\)\b",
    }

    extracted = {key: re.findall(pattern, text) for key, pattern in patterns.items()}
    return extracted

def print_extracted_patterns(extracted):
    for pattern_name, matches in extracted.items():
        print(f"{pattern_name.replace('_', ' ').title()}: {matches}")

example_texts = [
    """[Definition of “Queen”.] Omitted by A.O., 1961, Art. 2 and Sch. (w.e.f. the 23rd March, 1956).""",
    """In the case of Smith v. Jones, 123 F.2d 456 (2022), the court interpreted Section 123(a) of the Act. The hearing date was set for Aug 15, 2024.""",
    """[Adultery.] Rep. by the Offences of Zina (Enforcement of Hudood) Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979).""",
    """The Workmen's Breach of Contract (Repealing) Act, 1925 (III of 1925), s. 2 and Sch."""
]

for text in example_texts:
    print(f"Text: {text}\n")
    extracted = extract_patterns(text)
    print_extracted_patterns(extracted)
    print("\n" + "="*50 + "\n")


