import nltk
import re
import spacy
from nltk.tokenize import word_tokenize
from nltk.classify import apply_features
from nltk.corpus import conll2002

nlp = spacy.load("en_core_web_sm")


# Download the required NLTK resources if not already installed
nltk.download("conll2002")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Sample training data for intent classification
training_data = [
    ("Show sales data by year", "Show Group By"),
    ("Display product details", "Show"),
    # Add more training examples
]

# NER patterns
ner_patterns = [
    (r"\bin\b|\bby\b", "GROUP_BY"),
]


# Train the NER model
def train_ner(ner_patterns):
    tagged_sentences = conll2002.iob_sents()
    training_data = []

    for sentence in tagged_sentences:
        for word, tag, entity in sentence:
            features = {
                "word": word,
                "tag": tag,
            }
            label = entity if entity != 'O' else 'O'
            training_data.append((features, label))

    # Train the NER model using MaxentClassifier
    ner = nltk.MaxentClassifier.train(training_data, algorithm='iis', trace=0, max_iter=5)

    return ner


# Train the NER model
ner_model = train_ner(ner_patterns)

# Tokenization and intent classification
for query in ["Show sales data by year", "Display product details"]:
    tokens = word_tokenize(query)
    doc = nlp(query)
    intent = "Unknown"

    # Tokenization
    print(f"Tokens: {tokens}")

    # Intent classification
    for example, label in training_data:
        if " ".join(tokens).lower() in example.lower():
            intent = label
            break

    # Named Entity Recognition using the NER model
    entities = ner_model.classify_many([{"word": token, "tag": None} for token in tokens])

    print(f"User Query: '{query}'")
    print(f"Intent: {intent}")
    print(f"NER: {entities}")

    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
