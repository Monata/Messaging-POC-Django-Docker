from django.shortcuts import render
from ribbon.raiment.models import Item,Packlist,Folder,FolderHas,User
from rest_framework import generics, mixins
from ribbon.raiment.serializers import ItemSerializer,PacklistSerializer,FolderHasSerializer,FolderSerializer,UserSerializer
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



class Login(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClothingGroup(mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ClothingItem(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
