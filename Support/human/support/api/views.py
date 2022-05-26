from rest_framework.response import Response
from rest_framework.decorators import api_view

from website.models import Message
from .serializers import MessageSerializer

import random
from website import models
import joblib
import torch
from torch import nn


from nltk.stem.snowball import SnowballStemmer 
stemmer = SnowballStemmer("russian")

from model.model import model, vocabulary, preprocess_text


    



def get_predict(text):
    user_text_preprocessed  = preprocess_text(text)
    input_tensor = [vocabulary.sentence2indices(user_text_preprocessed)]
    input_tensor = torch.tensor(input_tensor).to(device=device)
    outputs = model(input_tensor)
    _, predicted = torch.max(outputs, dim=1)
    
    response = int(predicted)
    
    
    return response

index2category = {
    '0':'Animals',
    '1':'Dwelling',
    '2':'Custom Situation',
    '3':'Best Custom',
    '4':'Other',
    '5':'Transport',
    '6': 'Offer_Help',
}

situation2index = {
    'Slow':3,
    'Medium':2,
    'Fast':1,
    '----':10
}

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

def get_stemmed_names(custom):
    
    others_names = custom.other_names.split('|')
    
    stemmed_names = [stemmer.stem(name.lower()) for name in others_names ]

    return stemmed_names

def complementary_custom(user_text):
    customModels = models.Custom.objects.all()
    
    user_text_splited = user_text.lower().split()
    
    #Check each stemmed word if it is custom name
    complementary_text = ''
    

    user_text_splited_stemmed = [stemmer.stem(word) for word in user_text_splited]
    
    for custom in customModels:
        
        for stemmed_name in get_stemmed_names(custom):
            
            if stemmed_name in user_text_splited_stemmed:
                
                if custom.opened:
                    if custom.complementary_text:
                        complementary_text = custom.complementary_text
                        return complementary_text
                else:
                    complementary_text = f'На данный момент КПП {custom.ua_name} - {custom.md_name} не работает'

    return complementary_text

                
def get_faster_custom(CustomList):
    
    flow_customs = [situation2index[Custom.flow] for Custom in CustomList]
    faster_custom_indicator = min(flow_customs)
    faster_custom_index = flow_customs.index(faster_custom_indicator)
    faster_custom = CustomList[faster_custom_index]
    
    
    
    return (faster_custom.ua_name, faster_custom.md_name)
    
    
    
def complementary_BestCustom():
    customModels = models.Custom.objects.all()
    
    NorthCustoms = customModels.filter(position_custom='North')
    EastCustoms = customModels.filter(position_custom='East')
    WestCustoms = customModels.filter(position_custom='West')
    SouthCustoms = customModels.filter(position_custom='South')
    
    
    NorthFasterCustom = get_faster_custom(NorthCustoms)
    EastFasterCustom = get_faster_custom(EastCustoms)
    WestFasterCustom = get_faster_custom(WestCustoms)
    SouthFasterCustom = get_faster_custom(SouthCustoms)
    
    complementary_text = f"""    Самые быстрые пропускные пункты на вход в Молдову: @# С севера: {NorthFasterCustom[0]} - {NorthFasterCustom[1]} @# С юга: {SouthFasterCustom[0]} - {SouthFasterCustom[1]}  @# С запада: {WestFasterCustom[0]} - {WestFasterCustom[1]} @# С востока: {EastFasterCustom[0]} - {EastFasterCustom[1]} @# """
    
    
    
    return complementary_text
    





""" with open('vocabulary.pkl') as f:
    vocabulary = joblib.load(f) """

    

 






@api_view(['GET'])
def getData(request):
    items = Message.objects.all()
    serializer = MessageSerializer(items, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def get_anwer(request):
    serializer = MessageSerializer(data=request.data)
    
    
    
    returnText = ''
    
    
    if serializer.is_valid():
        serializer.save()
        
        user_text = serializer.data['text']
        
        
        #Preprocess text
        
        
        
       
        
         
        #Predict 
        predict = str(get_predict(user_text))
        
        print('\n\n\n', predict)
        
        categoryName = index2category[predict]
        categoryModel = models.Category.objects.filter(name=categoryName)[0]
        
        
        
        
        #Check if there are allowed to answer to this category
        if categoryModel.active:
            returnText = categoryModel.default_text
            
            #Complete answer if is allow
            if categoryModel.allow_complete:
                complementary_text = ''
                
                if categoryName == 'Custom Situation':
                    complementary_text = complementary_custom(user_text)
                elif categoryName == 'Best Custom':
                    complementary_text = complementary_BestCustom()

                returnText = f'{returnText}@#@#{complementary_text}'
            
                 
    return Response(returnText)