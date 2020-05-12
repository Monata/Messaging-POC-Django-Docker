from django.shortcuts import render
from raiment.models import Item,Packlist,Folder,FolderHas
from rest_framework import generics
from raiment.serializers import ItemSerializer,PacklistSerializer,FolderHasSerializer,FolderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ItemListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class PacklistListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Packlist.objects.all()
    serializer_class = PacklistSerializer

class FolderListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

class FolderHasListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = FolderHas.objects.all()
    serializer_class = FolderHasSerializer

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Correcto!'}
        return Response(content)