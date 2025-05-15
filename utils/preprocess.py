import os
import re
import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def clean_html(text):
    """Remove HTML tags from the text"""
    try:
        return BeautifulSoup(text, "html.parser").get_text()
    except Exception as e:
        return f"error occured in cleaning html:{e}"
    
    
def remove_special_chars(text):
    """Remove special characters and numbers"""
    try:
        return re.sub(r"[^a-zA-Z\s]", "", text)
    except Exception as e:
        return f"error occured in removing special character {e}"
def to_lower(text):
    try :
        """Convert text to lowercase"""
        return text.lower()
    except Exception as e:
        return f"error occured in converting to lower case {e}"
    
    


def remove_stopwords(text):
    """Remove common English stopwords"""
    try:
        tokens = text.split()
        tokens = [word for word in tokens if word not in stop_words]
        return " ".join(tokens)
    except Exception as e:
        return f"error occured in removing stop words {e}"
    


def lemmatize_text(text):
    """Lemmatize words to their base form"""
    try:
        tokens = text.split()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(tokens)
    except Exception as e:
        return f"erorr occured in lemmatinzing words {e}"
    

def preprocess_text(text):
    """Apply all preprocessing steps to the text"""
    try:
        text = clean_html(text)
        text = remove_special_chars(text)
        text = to_lower(text)
        text = remove_stopwords(text)
        text = lemmatize_text(text)
        return text
    except Exception as e:
        return f"error occured in preprocessing text {e}"
    

    