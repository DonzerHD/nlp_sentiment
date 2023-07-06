import string
import spacy

# Load the Spacy language model
nlp = spacy.load('en_core_web_sm')

# Create a list of stopwords
stop_words = nlp.Defaults.stop_words
custom_stopwords = ['nt', 'm', 's', 't', 've', 'feel', 'feeling', 'feelings', 'like', 'know', 'want', 'time', 'think', 'little']
stop_words = stop_words.union(custom_stopwords)

def preprocess_text(text):
    """
    Preprocesses the given text by converting to lowercase, removing punctuation, and removing stopwords.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: The preprocessed text.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    doc = nlp(text)
    text = " ".join([token.text for token in doc if not token.is_stop])
    return text
