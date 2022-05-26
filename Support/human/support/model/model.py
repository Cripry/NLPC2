import pandas as pd
import numpy as np

import torch
from torch import nn
from torch.utils.data import DataLoader

from nltk.stem.snowball import SnowballStemmer 
stemmer = SnowballStemmer("russian") 

from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS

from .Model.preprocessing import preprocess_text, rus_tokenizer, russian_stopwords
import os


from .Model.vocabulary import vocabulary




class GRU(nn.Module):
    def __init__(self, hidden_dim, output_dim, n_layers, num_words, drop_prob=0.2):
        super(GRU, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.embedding = nn.Embedding(num_words, hidden_dim)
        self.gru = nn.GRU(hidden_dim, hidden_dim, n_layers, batch_first=True,
                          dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.ReLU = nn.ReLU()

        

        
        
    def forward(self, x, h = None):
        x = self.embedding(x)
        out, h = self.gru(x)
        out = self.fc(self.ReLU(out[ : , -1]))
        return out
    




PAD_token = 0

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
      



device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
device



    
    

BASE_DIR = os.getcwd()


class GRU(nn.Module):
    def __init__(self, hidden_dim, output_dim, n_layers, num_words, drop_prob=0.2):
        super(GRU, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.embedding = nn.Embedding(num_words, hidden_dim)
        self.gru = nn.GRU(hidden_dim, hidden_dim, n_layers, batch_first=True,
                          dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.ReLU = nn.ReLU()

        

        
        
    def forward(self, x, h = None):
        x = self.embedding(x)
        out, h = self.gru(x)
        out = self.fc(self.ReLU(out[ : , -1]))
        return out






 

 





model = GRU(num_words=vocabulary.words_count, hidden_dim=16, output_dim=5, n_layers=2).to(device)
model_state_dict = torch.load(f'{os.path.join(BASE_DIR, "model/materials")}/5labels_0.9.pkl', map_location=torch.device('cpu'))
model.load_state_dict(model_state_dict)

model.eval()