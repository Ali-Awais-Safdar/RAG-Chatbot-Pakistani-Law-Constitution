import spacy
from spacy.tokens import Doc
from spacy.training import Example
from spacy.language import Language

nlp = spacy.load("en_core_web_sm")

@spacy.Language.component("legal_pos_tagger")
def legal_pos_tagger(doc):
    # Consider legal-specific rules and patterns
    for token in doc:
        # Example: Rule-based tagging for legal-specific terms
        if token.text in ["Section", "Act", "Court", "Defendant"]:
            token.tag_ = "LEGAL_TERM"
        # Add more rules as necessary
    return doc


nlp.add_pipe("legal_pos_tagger", after="tagger")

# Function to train the model
def train_legal_pos_tagger(train_data):
    optimizer = nlp.begin_training()
    for i in range(10):  # 10 iterations
        losses = {}
        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
    return nlp

# Example usage
text = "The court finds that the defendant violated Section 123 of the Act."
doc = nlp(text)
for token in doc:
    print(token.text, token.pos_, token.tag_)