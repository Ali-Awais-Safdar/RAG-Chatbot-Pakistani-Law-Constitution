import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer

def tokenize_legal_text(text):
    """
    Tokenizes legal text into sentences and words using custom patterns.

    Args:
        text (str): The input legal text to be tokenized.

    Returns:
        list of list of str: A nested list where each sublist contains tokens from a sentence.
    """
    citation_pattern = re.compile(r'''[sS]ect?i?o?n?\.?\s*\d+\([\da-zA-Z]\)-*[\da-zA-Z]*|[sS]ect?i?o?n?\.?\s*\d+\.*\d*|[aA]ct\s*\,?\.?\s*\(*\d+\)*\s\([IivV]*\sof\s\d*\)\,*\s*[sSvV]*\.*\s*\d*|[aA]ct\s*\,?\.?\s*\(*\d+\)*|[aA]rti?c?l?e?\s*\,?\.?\s*\(*\d+\)*\s\([IivV]*\sof\s\d*\)\,*\s*[sSvV]*\.*\s*\d*|[aA]rti?c?l?e?\.?\s*\d*\(*\d+\)*|[eE]lection\s*[cC]ommission\s*[pP]etition\sOrder\s*No\.\s*\d+\/\d+|ECP\s*Order\s*No\.\s*\d+\/\d+|[pP]akistan\s*[pP]enal\s*[cC]ode\s*\d{4}|[pP][pP][cC]\s*\d{4}|[pP]g\.\s*\d+|[pP]g\.\s*\d+|\d+\s*[sS]tat\.\s*\d+|[sS]tatute\s*\d+|[cC]l\.\s*\d+|[pP]t\.\s*\d+|[tT]bl\.\s*\d+|[fF]ig\.\s*\d+|[lL]n\.\s*\d+|[pP]ara\.\s*\d+|[aA]pp\.\s*\d+|[cC]h\.\s*\d+|[vV]ol\.\s*\d+|[rR]eg\.\s*\d+|[oO]rdinance\,*\s*\d+\s\([VIvi]*\sof\s\d*\)\,*\s*\w*\.*\s*\d*|[oO]rdinance\,*\s*\d+|[oO]rd\.\s*\d+|[aA]rt\.\s*\d+\(\d+\)\(\d+\)|SRO\s*\d+\(I\)\/\d{4}|\d+\s*[rsnt][tdh]\s*[aA]mendment|[aA]IR\s*\d+\s*[a-zA-Z]+\s*\d+|[pP][lL][dD]\s*\d{4}\s*[sS][cC]\s*\d+|[rR]ule\s*\d+\(\d+\)|[rR]ule\s*\d+\(\[a-zA-Z]\)|[rR]ule\s*\d+|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+\s*of\s*\d{4}|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+|[aA]nti\s*\-\s*[tT]errorism\s*[aA]ct\s*\d{4}|[rR]eview\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[cC]onstitution\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[iI]ncome\s*[tT]ax\s*[oO]rdinance\s\d{4}|[cC]ompanies\s*[oO]rdinance\s*\d{4}|[cC]ompanies\s*[oO]rd\s*\d{4}|[nN]otification\s*[nN]o\.*\s*\d+-\w*\/\d{4}|\(*[wE]\s*\.*[eE]\s*\.*[fF]\s*\.?\s*[tT][hH][eE]\s*\d+[rnts][thd]\s*\w*\s*\w*\s*o*f*\s*\w*\,*\s*\d*\)*|[aA]\.?\s*[oO]\.?\s*\,*\s*\d+''')
    citations = citation_pattern.findall(text)
    citations = [''.join(citation) for citation in citations]  
    placeholders = {f"__citation_{i}__": citation for i, citation in enumerate(citations)}
    for placeholder, citation in placeholders.items():
        text = text.replace(citation, placeholder)

    # Simplified sentence splitting based on common punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
   # print("Sentences after split:", sentences)  # Debugging statement

    # Custom word tokenizer pattern
    word_tokenizer = RegexpTokenizer(r'\w+(?:-\w+)*|\d+(?:\.\d+)?%?|\w+\.\w+|\S+')
    
    tokenized_text = []
    for sentence in sentences:
        words = word_tokenizer.tokenize(sentence)
        #print("Words in sentence:", words)  # Debugging statement
        tokenized_text.append(words)

    for i, sentence in enumerate(tokenized_text):
        tokenized_text[i] = [placeholders.get(word, word) for word in sentence]
    
    return tokenized_text

# sample_text = """Sec. 1.2 Art. 184(3) the Ordinance 784 court also sec. 6.8 Sec. 1.2 finds Art. 9 
# hiding act 67. Sec.3.5 Sec.6(8)-d defendant 114 Stat. 899 mr smith violated Sec. 3(a)-2 act. Art. 184(3) 
# on Pg. 45 also Sec. 4.66 constitution PPC 4444 important. Sec. 4 and Pakistan Penal Code 1860 implies that 
# Companies Ordinance 1984 often referenced refers to PLD 2020 SC 1 case law Rule 5(10). SRO 123(I)/2020 is also relevant. 18th Amendment brought significant changes. Presidential Order No. 1 of 1977 
# issued 3rd Amendment also cool refer Notification No. 1234-G/2020 Anti-Terrorism Act 1997 Review Petition No. 567/2020 
# filed check 2019 clc 123 relevant high court cases Income Tax Ordinance 2001 also cited 144 Stat. 789 also states 
# thing AIR 1990 SC 123 important precedent Constitution Petition No. 45/2021. ECP Order No. 123/2019 notable 
# Companies Ord 1984 also checkeddefinition queen omitted A.O., 1961 Art. 2 and school (w.e.f. the 23rd March, 1956) 
# case smith volume jones 123 f2d 456 2022 court interpreted Section 123(a) act hearing date set aug 15 2024 adultery 
# report offences zina enforcement hudood Ordinance, 1979 (VII of 1979), s. 19 (w.e.f the 10th day of February, 1979) workmens 
# breach contract repealing Act, 1925 (III of 1925), s. 2 school"""
# output = tokenize_legal_text(sample_text)
# print(output)