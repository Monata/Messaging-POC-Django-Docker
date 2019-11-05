from django.shortcuts import render
from raiment.models import Clothing
from rest_framework import generics
from raiment.serializers import ClothingSerializer
# Create your views here.

class ClothingListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
