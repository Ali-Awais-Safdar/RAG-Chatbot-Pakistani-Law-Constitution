from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
import json
import re
import os

# Text Normalization

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, '../data/legal_terms.json'), 'r') as f:
    legal_terms = json.load(f)

def normalize_legal_text(tokens):
    """
    Normalizes legal text tokens by performing several transformations:
    
    1. Matches and replaces custom legal terms.
    2. Corrects spelling of tokens.
    3. Lemmatizes tokens.
    4. Stems tokens.
    
    Args:
        tokens (list of str): The list of tokens to be normalized.
    
    Returns:
        list of str: The list of normalized tokens.
    """
    citation_pattern = re.compile(r'''[sS]ect?i?o?n?\.?\s*\d+\([\da-zA-Z]\)-*[\da-zA-Z]*|[sS]ect?i?o?n?\.?\s*\d+\.*\d*|[aA]ct\s*\,?\.?\s*\(*\d+\)*\s*\(*[IivV]*\s*of*\s*\d*\)*\,*\s*[sSvV]*\.*\s*\d*|[aA]rti?c?l?e?\.?\s*\(*\d+\)*\s*\(*[IivV]*\s*o*f*\s*\d*\)*\,*\s*[sSvV]*\.*\s*\d*|[aA]rt\.\s*\d+\(\d+\)|[eE]lection\s*[cC]ommission\s*[pP]etition\sOrder\s*No\.\s*\d+\/\d+|ECP\s*Order\s*No\.\s*\d+\/\d+|[pP]akistan\s*[pP]enal\s*[cC]ode\s*\d{4}|[pP][pP][cC]\s*\d{4}|[pP]g\.\s*\d+|[pP]g\.\s*\d+|\d+\s*[sS]tat\.\s*\d+|[sS]tatute\s*\d+|[cC]l\.\s*\d+|[pP]t\.\s*\d+|[tT]bl\.\s*\d+|[fF]ig\.\s*\d+|[lL]n\.\s*\d+|[pP]ara\.\s*\d+|[aA]pp\.\s*\d+|[cC]h\.\s*\d+|[vV]ol\.\s*\d+|[rR]eg\.\s*\d+|[oO]rdinance\,*\s*\d+\s*\(*[VIvi]*\s*o*f*\s*\d*\)*\s*\,*\s*\w*\.*\s*\d*|[oO]rd\.\s*\d+|[aA]rt\.\s*\d+\(\d+\)\(\d+\)|SRO\s*\d+\(I\)\/\d{4}|\d+\s*[rsnt][tdh]\s*[aA]mendment|[aA]IR\s*\d+\s*[a-zA-Z]+\s*\d+|[pP][lL][dD]\s*\d{4}\s*[sS][cC]\s*\d+|[rR]ule\s*\d+\(\d+\)|[rR]ule\s*\d+\(\[a-zA-Z]\)|[rR]ule\s*\d+|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+\s*of\s*\d{4}|[pP]residential\s*[oO]rder\s*[nN]o\.*\s*\d+|[aA]nti\s*\-\s*[tT]errorism\s*[aA]ct\s*\d{4}|[rR]eview\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[cC]onstitution\s*[pP]etition\s*[nN]o\.*\s*\d+\/\d{4}|[iI]ncome\s*[tT]ax\s*[oO]rdinance\s\d{4}|[cC]ompanies\s*[oO]rdinance\s*\d{4}|[cC]ompanies\s*[oO]rd\s*\d{4}|[nN]otification\s*[nN]o\.*\s*\d+-\w*\/\d{4}|\(*[wE]\s*\.*[eE]\s*\.*[fF]\s*\.?\s*[tT][hH][eE]\s*\d+[rnts][thd]\s*\w*\s*\w*\s*o*f*\s*\w*\,*\s*\d*\)*|[aA]\.?\s*[oO]\.?\s*\,*\s*\d+''')
    placeholders = {}
    normalized_tokens = []
    i = 0
    citation_index = 0
    final_tokens = []

    while i < len(tokens):
        token = tokens[i]
        if citation_pattern.match(token):
            placeholder = f"__CITATION_{citation_index}__"
            placeholders[placeholder] = token
            normalized_tokens.append(placeholder)
            citation_index += 1
        else:
            normalized_tokens.append(token)
        i += 1

    i = 0
    final_tokens = []
    while i < len(normalized_tokens):
        token = normalized_tokens[i]
        if token in placeholders:
            final_tokens.append(token)
            i += 1
            continue

        matched = False
        for term in legal_terms:
            term_tokens = term.split()
            if normalized_tokens[i:i+len(term_tokens)] == term_tokens:
                replacement_tokens = legal_terms[term.lower()].split()
                final_tokens.extend(replacement_tokens)
                i += len(term_tokens)
                matched = True
                break

        if not matched:
            corrected_token = str(TextBlob(token).correct())
            lemma = lemmatizer.lemmatize(corrected_token.lower())
            stem = stemmer.stem(lemma)
            final_tokens.append(stem)
            i += 1

    final_tokens = [placeholders.get(token, token) for token in final_tokens]

    return final_tokens

# tokens = ["Sec. 1.2", "court", "finds", "Sec.3.5", "defendant", "mr", "smith", "violated", "Sec. 3(a)-2", "Act", "according", "Ordinance 1444", "far", "more", "crimes", "than", "Sec. 3(a)-12", "acts"]
# print("\nInput:\t" + str(tokens) + "\nOutput:\t" + str(normalize_legal_text(tokens)))
