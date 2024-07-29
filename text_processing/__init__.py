def tokenize_legal_text(text):
    """
    Tokenizes legal text into sentences and words using custom patterns.

    Args:
        text (str): The input legal text to be tokenized.

    Returns:
        list of list of str: A nested list where each sublist contains tokens from a sentence.
    """
    # Simplified sentence splitting based on common punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
   # print("Sentences after split:", sentences)  # Debugging statement

    # Custom word tokenizer pattern
    word_tokenizer = RegexpTokenizer(r'\w+(?:-\w+)*|\d+(?:\.\d+)?%?|\w+\.\w+|\S+')
    
    tokenized_text = []
    for sentence in sentences:
        words = word_tokenizer.tokenize(sentence)
    #    print("Words in sentence:", words)  # Debugging statement
        tokenized_text.append(words)
    
    return tokenized_text
