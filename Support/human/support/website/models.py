from django.db import models
from nltk.stem.snowball import SnowballStemmer 
stemmer = SnowballStemmer("russian")
from transliterate import translit

# Create your models here.



class Custom(models.Model):
    
    FLOW_CHOICES = [
        ('Slow', 'Slow'),
        ('Medium', 'Medium'),
        ('Fast', 'Fast'),
        ('----', '----'),
    ]
    POSITION_CUSTOM = [
        ('North','North'),
        ('East', 'East'),
        ('West','West'),
        ('South','South')
    ]
    
    
    md_name = models.CharField(max_length=100, blank=False, null=False)
    ua_name = models.CharField(max_length=100, blank=False, null=False)
    opened = models.BooleanField(verbose_name='Opened', default=True)
    flow = models.CharField(max_length=9, choices=FLOW_CHOICES, default="----")
    complementary_text = models.TextField(blank=True, null=True)
    position_custom = models.CharField(max_length=10, choices=POSITION_CUSTOM, default="North")
    other_names = models.CharField(max_length=255, blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.md_name} --- {self.ua_name}'
    

    
    
    
    
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    default_text = models.TextField(blank=True, null=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    allow_complete = models.BooleanField(verbose_name='Permission to Complete', default=True)
    
    
    def __str__(self):
        return f'{self.name}'
    
    
class Message(models.Model):
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text