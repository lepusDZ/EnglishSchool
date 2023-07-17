from django.db import models
from django_quill.fields import QuillField
from django.urls import reverse

class Main(models.Model):
    title = models.CharField(max_length = 150, blank = True)

    def __str__(self):
        return self.title
    
class Dish(models.Model):
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    
    def __str__(self):
        return self.title

class Ingredients(models.Model):

    def __str__(self):
        return self.title
