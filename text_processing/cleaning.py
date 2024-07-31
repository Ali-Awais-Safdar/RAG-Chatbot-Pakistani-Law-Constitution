import json
import re
import os

# Text Cleaning

# load custom legal stopwords and abbreviations
current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, '../data/legal_abbreviations.json'), 'r') as f:
    legal_abbreviations = json.load(f)
with open(os.path.join(current_dir, '../data/legal_stopwords.json'), 'r') as f:
    legal_stopwords = json.load(f)

def clean_legal_text(text):
    """
    Cleans and normalizes legal text by performing several transformations:
    
    1. Normalizes case while preserving specific terms.
    2. Removes stopwords.
    3. Expands legal abbreviations.
    4. Removes leading numbers, underscores and periods.
    5. Removes punctuation.
    6. Normalizes whitespace.
    
    Args:
        text (str): The legal text to be cleaned.
    
    Returns:
        str: The cleaned and normalized legal text.
    """
    # identifying and replacing citations with placeholders
    citation_pattern = re.compile(r'''[sS]ec\.?\s*\d+\.\d+|[sS]ec\.\s*\d+\([\da-zA-Z]\)-[\da-zA-Z]|
                                  [aA]rt\.\s*\d+|[aA]rt\.\s*\d+\(\d+\)|ECP\s*Order\s*No\.\s*\d+\/\d+|[pP]akistan\s*[pP]enal\s*[cC]ode\s*\d{4}|[pP][pP][cC]\s*\d{4}|[pP]g\.\s*\d+|[pP]g\.\s*\d+|
                                  [sS]tat\.\s*\d+|[sS]tatute\s*\d+|
                                  [cC]l\.\s*\d+|[pP]t\.\s*\d+|[tT]bl\.\s*\d+|[fF]ig\.\s*\d+|
                                  [lL]n\.\s*\d+|[pP]ara\.\s*\d+|[aA]pp\.\s*\d+|
                                  [cC]h\.\s*\d+|[vV]ol\.\s*\d+|[rR]eg\.\s*\d+|
                                  [oO]rd\.\s*\d+|[oO]rdinance\s*\d+|[aA]rt\.\s*\d+\(\d+\)\(\d+\)|
                                  SRO\s*\d+\(I\)\/\d{4}|
                                  \d+th\s+Amendment|\d+st\s+Amendment|\d+nd\s+Amendment|\d+rd\s+Amendment|\w+th\s+Amendment|\w+rd\s+Amendment|\w+nd\s+Amendment|\w+st\s+Amendment|
                                  [aA]IR\s*\d+\s*[a-zA-Z]+\s*\d+|[cC]onstitution\s*[pP]etition\s*No\.\s*\d+\/\d+|
                                  [eE]lection\s*[cC]ommission\s*[pP]etition\sOrder\s*No\.\s*\d+\/\d+
                                  ''')
    citations = citation_pattern.findall(text)
    citations = [''.join(citation) for citation in citations]  # Join tuple elements to form citation strings
    print(citations)
    placeholders = {f"__citation_{i}__": citation for i, citation in enumerate(citations)}
    for placeholder, citation in placeholders.items():
        text = text.replace(citation, placeholder)
    
    # normalizing case and preserve specific terms
    text = ' '.join([word if word in legal_abbreviations else word.lower() for word in text.split()])

    # removing stopwords
    words = text.split()
    words = [word for word in words if word not in legal_stopwords]
    text = ' '.join(words)  

    # expanding the abbreviations 
    for abbr, expansion in legal_abbreviations.items():
        escaped_abbr = re.escape(abbr)
        pattern = r'(\W|^)' + escaped_abbr + r'(?=\s|\Z|\W(?!\w))'
        replacement = r'\1' + expansion
        text = re.sub(pattern, replacement, text)
        
    # removing leading numbers and periods
    text = re.sub(r'^\d+\.\s*', '', text)

    # removing punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # normalizing whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # preserving the citations by replacing the placeholders
    for placeholder, citation in placeholders.items():
        text = text.replace(placeholder, citation)

    return text

#sample_text = "Sec. 1.2 and the Art. 184(3) The Ordinance 784 court also sec. 6.8 finds Art. 9 from Sec.3.5 and Sec.6(8)-d that the defendant 114 Stat. 899 Mr. Smith violated Sec. 3(a)-2 of the Act."
sample_text = """
Art. 184(3) on Pg. 45 also Sec. 4.66 of the Constitution PPC 4444 is important. Sec. 4 of the Pakistan Penal Code 1860 and Companies Ordinance 1984 
are often referenced. Refer to PLD 2020 SC 1 for case law. Rule 5(1) and SRO 123(I)/2020 are also relevant.
The 18th Amendment brought significant changes. Presidential Order No. 1 of 1977 was issued. The 3rd Amendment is also cool
Refer to Notification No. 1234-G/2020 and The Anti-Terrorism Act 1997. Review Petition No. 567/2020 was filed.
Check 2019 CLC 123 for relevant High Court cases. The Income Tax Ordinance 2001 is also cited.
AIR 1990 SC 123 is an important precedent. Constitution Petition No. 45/2021 and ECP Order No. 123/2019 are notable.
Companies Ord 1984 should also be checked.
"""
print("CLEANED TEXT: " + clean_legal_text(sample_text))
