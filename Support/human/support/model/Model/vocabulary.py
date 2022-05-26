import os
import numpy
import torch
import numpy as np
from .preprocessing import  rus_tokenizer, preprocess_text, russian_stopwords
import pandas as pd


class Vocabulary:
    def __init__(self):
        self.PAD_TOKEN = 0
        self.word2index = {}
        self.word2count = {}
        self.index2word = { self.PAD_TOKEN: 'PAD' }
        self.words_count = 1
        self.tokenizer = rus_tokenizer
        self.max_length = 0 




    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.words_count
            self.word2count[word] = 1
            self.index2word[self.words_count] = word
            self.words_count += 1
        else:
            self.word2count[word] += 1

    def add_sentence(self, sentence):
        sentence = preprocess_text(sentence)
        tokens = self.tokenizer(sentence)

        tokens = [token for token in tokens if token 
                  not in russian_stopwords and len(token) > 1]

        if len(tokens) > self.max_length:
            self.max_length = len(tokens)

        for token in tokens:
            self.add_word(token)

    def sentence2indices(self, sentence):
        sentence = preprocess_text(sentence)

        #Return None if string has more than 15 tokens
        tokens = self.tokenizer(sentence)
        if len(tokens) <= 15:
          result = [ self.PAD_TOKEN ] * self.max_length  
          idx = 0
          for token in tokens:
              if token in self.word2index:
                  result[idx] = self.word2index[token]
                  idx += 1

          return result
        else:
          return np.nan



BASE_DIR = os.getcwd()
vocabulary = Vocabulary()


df = pd.read_csv(f'{os.path.join(BASE_DIR, "model/materials")}/5labels_0.9.csv')
df = df.drop(['Unnamed: 0'], axis=1)


for text in df['questions']:
    vocabulary.add_sentence(text)


print(vocabulary.words_count, '\n\n\n\n\n')