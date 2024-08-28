from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import nltk
import numpy as np
import spacy
from text_processing import clean_legal_text, tokenize_legal_text

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nlp = spacy.load('en_core_web_sm')

def preprocess_question(question):
    """
    Preprocesses the input question by applying NER and POS tagging to extract key elements and emphasize entities.

    Args:
        question (str): The raw legal question.

    Returns:
        tuple: A tuple containing:
          - str: The refined question with key entities highlighted.
          - list: A list of tokens identified as important based on POS tagging.
          - list: A list of named entities found in the question.
    """
    if not question or not isinstance(question, str):
        return None
    # Implement question preprocessing logic
    # Consider using POS tagging to identify key elements
    processed_question = question.lower().strip()
    
    doc = nlp(processed_question)
    # extract POS tags and NER information
    tokens = [(token.text, token.pos_) for token in doc]
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    refined_question_tokens = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB', 'PROPN']]
    # highlight or emphasize key entities in the question
    entity_map = {ent.text: f"[{ent.text}]" for ent in doc.ents}
    refined_question = " ".join([entity_map.get(token.text, token.text) for token in doc])

    # print("Refined Question with Entities Highlighted:", refined_question)
    return refined_question, refined_question_tokens, entities

def retrieve_relevant_segments(question, documents):
    """
    Retrieves the most relevant document segments that may contain the answer to the legal question.

    Args:
        question (str): The processed legal question.
        documents (list of str): The corpus of legal documents.

    Returns:
        list of str: The top relevant document segments.
    """
    if not question or not isinstance(question, str) or not documents:
        return None
    # Implement document retrieval logic
    # Consider using TF-IDF or more advanced retrieval methods
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    # compute cosine similarity between the question and document segments
    similarities = cosine_similarity(question_vector, doc_vectors).flatten()

    # get the top 5 most relevant document segments
    top_indices = np.argsort(similarities)[-5:][::-1]
    relevant_segments = [documents[i] for i in top_indices]

    return relevant_segments

def generate_answer(question, context, model, tokenizer, entities):
    """
    Generates an answer to the legal question using a fine-tuned language model and the relevant context from legal documents.

    Args:
        question (str): The preprocessed legal question.
        context (str): The context string containing the relevant document segments.
        model (PreTrainedModel): The fine-tuned language model for question answering.
        tokenizer (PreTrainedTokenizer): The tokenizer corresponding to the model.
        entities (list): A list of named entities extracted from the question, which can be used for refining the context or processing the answer.

    Returns:
        tuple: A tuple containing:
          - str: The raw answer generated by the model.
          - float: The confidence score associated with the answer.
    """
    if not question or not isinstance(question, str) or not context or not tokenizer:
        return None
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    result = qa_pipeline(question=question, context=context)

    return result['answer'], result['score']

def postprocess_answer(answer, relevant_segments, question, confidence_score):
    """
    Post-process the answer by adding citations and confidence scores.
    
    Parameters:
    - answer: The initial answer generated by the QA model.
    - relevant_segments: The document segments that were retrieved.
    - question: The original question asked.
    - qa_result: The result from the QA model that includes the confidence score.
    
    Returns:
    - processed_answer: The final processed answer with citations and confidence score.
    """
    processed_answer = answer.strip()

    # # Generate citations from relevant segments
    # citations = []
    # for i, segment in enumerate(relevant_segments):
    #     # Assuming you have a way to reference the document (e.g., title, page number, etc.)
    #     citation = f"[Document {i+1}: Excerpt from '{segment[:30]}...']"
    #     citations.append(citation)
    
    # # Add citations to the answer
    # processed_answer += f"\n\nCitations:\n" + "\n".join(citations)

    # calculate the confidence score
    confidence_score = confidence_score * 100  # assuming 'score' is a probability
    processed_answer += f" (Confidence Score: {confidence_score:.2f}%)"

    return processed_answer

def legal_qa_system(question, documents, model, tokenizer):
    """
    The main pipeline that handles the complete legal question answering process:
    preprocessing the question, retrieving relevant document segments, generating an answer,
    and post-processing the answer.

    Args:
        question (str): The legal question to be answered.
        documents (list of str): The corpus of legal documents to search through.
        model (PreTrainedModel): The fine-tuned language model for question answering.
        tokenizer (PreTrainedTokenizer): The tokenizer corresponding to the model.

    Returns:
        str: The final answer to the legal question.
    """
    if not question or not isinstance(question, str) or not documents or not isinstance(documents, list):
        return None
    
    processed_question, tokens, entities = preprocess_question(question)
    relevant_segments = retrieve_relevant_segments(processed_question, documents)
    context = " ".join(relevant_segments)
    raw_answer, confidence_score = generate_answer(processed_question, context, model, tokenizer, entities)
    final_answer = postprocess_answer(raw_answer, relevant_segments, processed_question, confidence_score)
    
    return final_answer

def load_legal_documents():
    """
    Loads the corpus of legal documents that will be used for retrieving relevant information.

    Returns:
        list of str: A list of legal documents as strings.
    """
    # Implement logic to load legal documents
    return [
        "Under Pakistani law, copyright infringement is a punishable offense.",
        "The penalty for copyright infringement may include fines and imprisonment.",
        "The Copyright Ordinance 1962 outlines the penalties for copyright infringement.",
        "Copyright law in Pakistan is governed by the Copyright Ordinance of 1962.",
        "In Pakistan, copyright infringement is considered a serious offense."
    ]
def load_sample_documents():
    """
    Loads the corpus of legal documents that will be used for retrieving relevant information.

    Returns:
        list of str: A list of legal documents as strings.
    """
    # Implement logic to load legal documents
    return [
        "Under Pakistani law, copyright infringement is a punishable offense.",
        "The penalty for copyright infringement may include fines and imprisonment.",
        "The Copyright Ordinance 1962 outlines the penalties for copyright infringement.",
        "Copyright law in Pakistan is governed by the Copyright Ordinance of 1962.",
        "In Pakistan, copyright infringement is considered a serious offense."
    ]
def load_finetuned_model():
    model_name = "deepset/roberta-base-squad2"
    fine_tuned_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return fine_tuned_model, tokenizer
    # # Load the fine-tuned model and tokenizer
    # fine_tuned_model = AutoModelForQuestionAnswering.from_pretrained('./fine_tuned_model')
    # tokenizer = AutoTokenizer.from_pretrained('./fine_tuned_model')

