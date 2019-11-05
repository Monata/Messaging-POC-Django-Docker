from django.db import models

# Create your models here.
class Clothing(models.Model):
    #Class to store information about our clothing
    type = models.CharField(max_length= 50)
    color_tag = models.CharField(max_length= 50)
    brand = models.CharField(max_length=50)
