from django.shortcuts import render
from raiment.models import Item,Packlist
from rest_framework import generics
from raiment.serializers import ItemSerializer,PacklistSerializer
# Create your views here.

class ItemListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class PacklistListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Packlist.objects.all()
    serializer_class = PacklistSerializer