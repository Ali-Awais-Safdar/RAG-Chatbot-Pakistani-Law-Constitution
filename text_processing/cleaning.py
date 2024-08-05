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
    citation_pattern = re.compile(r'''[sS]ect?i?o?n?\.?\s*\d+\([\da-zA-Z]\)-*[\da-zA-Z]*|[sS]ect?i?o?n?\.?\s*\d+\.*\d*|[aA]ct\s*\,?\.?\s*\(*\d+\)*\s*\(*[IivV]*\s*of*\s*\d*\)*\,*\s*[sSvV]*\.*\s*\d*|[aA]rti?c?l?e?\.?\s*\(*\d+\)*\s*\(*[IivV]*\s*o*f*\s*\d*\)*\,*\s*[sSvV]*\.*\s*\d*|[aA]rt\.\s*\d+\(\d+\)|[eE]lection\s*[cC]ommission\s*[pP]etition\sOrder\s*No\.\s*\d+\/\d+|ECP\s*Order\s*No\.\s*\d+\/\d+|[pP]akistan\s*[pP]enal\s*[cC]ode\s*\d{4}|[pP][pP][cC]\s*\d{4}|[pP]g\.\s*\d+|[pP]g\.\s*\d+|\d+\s*[sS]tat\.\s*\d+|[sS]tatute\s*\d+|[cC]l\.\s*\d+|[pP]t\.\s*\d+|[tT]bl\.\s*\d+|[fF]ig\.\s*\d+|[lL]n\.\s*\d+|[pP]ara\.\s*\d+|[aA]pp\.\s*\d+|[cC]h\.\s*\d+|[vV]ol\.\s*\d+|[rR]eg\.\s*\d+|[oO]rdinance\,*\s*\d+\s*\(*[VIvi]*\s*o*f*\s*\d*\)*\s*\,*\s*\w*\.*\s*\d*|[oO]rd\.\s*\d+|[aA]rt\.\s*\d+\(\d+\)\(\d+\)|SRO\s*\d+\(I\)\/\d{4}|\d+\s*[rsnt][tdh]\s*[aA]mendment|[aA]IR\s*\d+\s*[a-zA-Z]+\s*\d+|[pP][lL][dD]\s*\d{4}\s*[sS][cC]\s*\d+|[rR]ule\s*\d+\(\d+\)|[rR]ule\s*\d+\(\[a-zA-Z]\)|[rR]ule\s*\d+|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+\s*of\s*\d{4}|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+|[aA]nti\s*\-\s*[tT]errorism\s*[aA]ct\s*\d{4}|[rR]eview\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[cC]onstitution\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[iI]ncome\s*[tT]ax\s*[oO]rdinance\s\d{4}|[cC]ompanies\s*[oO]rdinance\s*\d{4}|[cC]ompanies\s*[oO]rd\s*\d{4}|[nN]otification\s*[nN]o\.*\s*\d+-\w*\/\d{4}|\(*[wE]\s*\.*[eE]\s*\.*[fF]\s*\.?\s*[tT][hH][eE]\s*\d+[rnts][thd]\s*\w*\s*\w*\s*o*f*\s*\w*\,*\s*\d*\)*|[aA]\.?\s*[oO]\.?\s*\,*\s*\d+''')
    citations = citation_pattern.findall(text)
    citations = [''.join(citation) for citation in citations]  # Join tuple elements to form citation strings
    #print("\nCITATIONS:\t" + str(citations))
    placeholders = {f"__citation_{i}__": citation for i, citation in enumerate(citations)}
    for placeholder, citation in placeholders.items():
        text = text.replace(citation, placeholder)
    
    # normalizing case and preserve specific terms
    text = ' '.join([word if word in legal_abbreviations else word.lower() for word in text.split()])

    # removing stopwords
    words = [word for word in text.split() if word not in legal_stopwords]
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

    # preserving the citations by replacing the placeholders
    for placeholder, citation in placeholders.items():
        text = text.replace(placeholder, citation)

    # remove underscores
    text = text.replace('_', '')

    # normalizing whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# sample_text = """
# Sec. 1.2 and the Art. 184(3) The Ordinance 784 court also sec. 6.8 Sec. 1.2 finds Art. 9 hiding Act. 67 from Sec.3.5 and Sec.6(8)-d that the defendant 114 Stat. 899 Mr. Smith violated Sec. 3(a)-2 of the Act.
# Art. 184(3) on Pg. 45 also Sec. 4.66 of the Constitution PPC 4444 is important. Sec. 4 of the Pakistan Penal Code 1860 and Companies Ordinance 1984 
# are often referenced. Refer to PLD 2020 SC 1 for case law. Rule 5(10) and SRO 123(I)/2020 are also relevant.
# The 18th Amendment brought significant changes. Presidential Order No. 1 of 1977 was issued. The 3rd Amendment is also cool
# Refer to Notification No. 1234-G/2020 and The Anti-Terrorism Act 1997. Review Petition No. 567/2020 was filed.
# Check 2019 CLC 123 for relevant _ High Court__ cases. The Income Tax Ordinance 2001 is also cited. The 144 Stat. 789 also states the same thing.
# AIR 1990 SC 123 is an important precedent. Constitution Petition No. 45/2021 and ECP Order No. 123/2019 are notable.
# Companies Ord 1984 should also be checked.[Definition of “Queen”.] Omitted by A.O., 1961, Art. 2 and Sch. (w.e.f. the 23rd March, 1956).
#     In the case of Smith v. Jones, 123 F.2d 456 (2022), the court interpreted Section 123(a) of the Act. The hearing date was set for Aug 15, 2024.,
#     [Adultery.] Rep. by the Offences of Zina (Enforcement of Hudood) Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979).,
#     The Workmen's Breach of Contract (Repealing) Act, 1925 (III of 1925), s. 2 and Sch."""
# print("\nORIGINAL TEXT:\t" + sample_text)
# print("\nCLEANED TEXT:\t" + clean_legal_text(sample_text))
