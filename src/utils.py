import os
import re
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FakeNewsDetection")

# Hardcoded English Stopwords (standard NLTK list)
stopwords_english = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def simple_stem(word):
    """
    A simple suffix-stripping heuristic that acts as a fast, pure-Python stemmer.
    """
    if len(word) > 4:
        if word.endswith('ing'):
            return word[:-3]
        elif word.endswith('ly'):
            return word[:-2]
        elif word.endswith('ed'):
            return word[:-2]
        elif word.endswith('es'):
            return word[:-2]
        elif word.endswith('s') and not word.endswith('ss'):
            return word[:-1]
    return word

def clean_text(text):
    """
    Cleans raw news text using pure Python:
    1. Lowercases the input.
    2. Removes URL paths, HTML tags, and non-alphabetic characters.
    3. Splits into tokens.
    4. Removes stop words.
    5. Applies basic suffix stemming.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs, HTML tags, and non-alphabetic/whitespace characters
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # 3. Tokenize by splitting
    tokens = text.split()
    
    # 4 & 5. Filter stop words and apply simple stemming
    cleaned_tokens = []
    for word in tokens:
        if word not in stopwords_english:
            stemmed = simple_stem(word)
            if stemmed:
                cleaned_tokens.append(stemmed)
                
    return " ".join(cleaned_tokens)
