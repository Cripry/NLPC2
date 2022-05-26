from nltk.tokenize import  word_tokenize
import nltk
nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords
import os
import string

import torch
from torch import nn
from torch.utils.data import DataLoader
from string import punctuation


russian_stopwords = stopwords.words('russian')
    
import pymorphy2
morph = pymorphy2.MorphAnalyzer()



def lemmatizer_rus(word):
  word_lemm = morph.parse(word)[0].normal_form
  return word_lemm



def clear_word(word) -> str:
    '''
    Function to clear word from non alphabetical symbols 
    
    Parameters:
        word : string with word to be cleared

    Output:
        string with alphabetical symbols
    '''
    for char in word:
        if not char.isalpha() and char != '-' and char != ' ':
            word = word.replace(char, '')

    letters = [char for char in string.ascii_letters]
    for char in letters:
        word = word.replace(char, '')
        
    
    return word


def rus_tokenizer(text):

    tokens = word_tokenize(text, language='russian')
    return tokens



def preprocess_text(text):
    tokens = rus_tokenizer(text)
    tokens = [lemmatizer_rus(clear_word(token)) for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(token for token in tokens if token)
    
    return text

