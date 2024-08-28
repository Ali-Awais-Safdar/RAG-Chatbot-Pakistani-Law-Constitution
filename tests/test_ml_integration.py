from ml_integration import legal_qa_system, load_sample_documents, postprocess_answer, retrieve_relevant_segments, preprocess_question, generate_answer, load_finetuned_model
import unittest
from unittest.mock import patch

from safetensors.torch import load_model

class TestLegalQASystem(unittest.TestCase):

    def test_legal_qa_system(self):
        model, tokenizer = load_finetuned_model()
        documents = load_sample_documents()
        result = legal_qa_system("What is the penalty for copyright infringment?", documents, model, tokenizer)
        expected_phrases = ["fines", "imprisonment"]

        # Check if all the expected phrases are in the answer
        for phrase in expected_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, result, f"The answer should contain the word '{phrase}'.")

    def test_empty_question(self):
        result = legal_qa_system("", ["Document 1"], "model", "tokenizer")
        self.assertIsNone(result)

    def test_empty_documents(self):
        question = "What is the penalty for copyright infringement under Pakistani law?"
        result = legal_qa_system(question, [], "model", "tokenizer")
        self.assertIsNone(result)

    def test_wrong_document_type(self):
        question = "What is the penalty for copyright infringement under Pakistani law?"
        result = legal_qa_system(question, " ", "model", "tokenizer")
        self.assertIsNone(result)
