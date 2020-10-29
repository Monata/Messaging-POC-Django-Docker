from django.shortcuts import render
from raiment.models import Item,Packlist,Folder,FolderHas,User,UserProfile,ItemType,FolderInventory,Inventory,Entry,PacklistInventory
from rest_framework import generics
from raiment.serializers import ItemSerializer,PacklistSerializer,FolderHasSerializer,FolderSerializer,UserSerializer,hUserSerializer,ItemTypeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes,api_view
import json
from raiment.methods import detect
from ribbon.settings import MODEL,COLOURS

# Create your views here.

@permission_classes([])
class ItemListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


@permission_classes([IsAdminUser])
class TypeCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

class GetAllItems(generics.GenericAPIView):
    def get(self, request):
        qs = Inventory.objects.filter(user=request.user)
        content = {"items": []}
        for j in qs:
            item = j.entry.item
            d = {}
            d["id"] = j.entry.id
            d["colour"] = item.colour
            d["image_link"] = item.image_link
            d["material"] = item.material
            d["price"] = item.price
            d["size"] = item.size
            d["brand"] = item.brand
            d["type"] = item.type.id
            d["type_name"] = item.type.name
            d["wearcount"] = j.entry.wearcount
            d["weather"] = item.weather
            content["items"].append(d)
        return Response(content)


class AddToInventory(generics.GenericAPIView):
    def get(self, request):
        itemID = request.GET['itemID']
        n_entry = Entry.objects.create(item_id=itemID, wearcount=0, count=1)
        Inventory.objects.create(entry=n_entry,user=request.user)
        content = {"items": [n_entry.id]}
        return Response(content)


class GetClothesWeather(generics.GenericAPIView):
    def get(self, request):
        qs = Inventory.objects.filter(user=request.user)
        content = {"items":[]}
        weather = request.GET['weather']
        for j in qs:
            item = j.entry.item
            if(weather != item.weather):
                continue
            d = {}
            d["id"] = j.entry.id
            d["colour"] = item.colour
            d["image_link"] = item.image_link
            d["material"] = item.material
            d["price"] = item.price
            d["size"] = item.size
            d["brand"] = item.brand
            d["type"] = item.type.id
            d["type_name"] = item.type.name
            d["wearcount"] = j.entry.wearcount
            d["weather"] = item.weather
            content["items"].append(d)
        return Response(content)



class PacklistListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    serializer_class = PacklistSerializer
    def get_queryset(self):
        user = self.request.user
        return Packlist.objects.filter(packlistinventory__in =  PacklistInventory.objects.filter(user=user))



class FolderListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FolderHasListCreate(generics.ListCreateAPIView):
    #to return every object stored and add new objects using the generic view
    queryset = FolderHas.objects.all()
    serializer_class = FolderHasSerializer


class HelloView(APIView):
    def get(self, request):
        id = request.user.id
        content = {'message': id}
        return Response(content)

@authentication_classes([])
@permission_classes([])
class SignUp(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })

class AddToPacklist(generics.GenericAPIView):
    def post(self,args):
        try:
            packlist = Packlist.objects.get(id = self.request.POST['packlist'])
        except Packlist.DoesNotExist:
            return Response("No such packlist exists")
        if(PacklistInventory.objects.filter(packlist=packlist,user=self.request.user).first()):
            for j in self.request.POST['entries'].split(','):
                i = int(j)
                entry = Entry.objects.get(id = i)
                FolderHas.objects.create(folder=packlist.folder,entry = entry)
            return Response("added " + self.request.POST['entries'] +" to the packlist id with " + self.request.POST['packlist'])
        else:
            return Response("This packlist is not yours")

class GetPacklistContent(generics.GenericAPIView):
    def get(self,args):
        try:
            packlist = Packlist.objects.get(id = self.request.GET['packlist'])
        except Packlist.DoesNotExist:
            return Response("No such packlist exists")
        if(PacklistInventory.objects.filter(packlist=packlist,user=self.request.user).first()):
            qs =FolderHas.objects.filter(folder=packlist.folder)
            content = []
            for j in qs:
                item = j.entry.item
                d = {}
                d["id"] = j.entry.id
                d["colour"] = item.colour
                d["image_link"] = item.image_link
                d["material"] = item.material
                d["price"] = item.price
                d["size"] = item.size
                d["brand"] = item.brand
                d["type"] = item.type.id
                d["type_name"] = item.type.name
                d["wearcount"] = j.entry.wearcount
                d["weather"] = item.weather
                content.append(d)
            return Response(content)
        else:
            return Response("This packlist is not yours")

class CreateToPacklist(generics.GenericAPIView):
    def post(self,args):
        folder = Folder.objects.create()
        p = Packlist.objects.create(date= self.request.POST['date'],folder=folder,name=self.request.POST['name'])
        PacklistInventory.objects.create(user= self.request.user,packlist=p)
        fail = []
        succ = []
        for j in self.request.POST['entries'].split(','):
            i = int(j)
            print(i,"wololo")
            entry = Entry.objects.get(id = i)
            if(Inventory.objects.filter(user=self.request.user,entry=entry).first()):
                FolderHas.objects.create(folder=p.folder,entry = entry)
                succ.append(i)
            else:
                fail.append(i)
        message = {"id":p.id,"success":succ,"fail":fail}
        return Response(message)



class ObjectDetect(generics.GenericAPIView):
        def post(self,args):
            img = self.request.POST['base64']
            result = detect(MODEL,img)
            euclidean = lambda x, y: (x[0]-y[2])**2 + (x[1]-y[1])**2 + (x[2]-y[0])**2
            m_256 = lambda x: (x[0]*256,x[1]*256,x[2]*256)
            min_dist = (256 * 256) * 4
            alt_min_dist = (256 * 256) * 4
            result_colour = "Errory_boii"
            alt_colour = "Errory_boi"
            for i in COLOURS:
                d = euclidean(COLOURS[i],m_256(result[-1]))
                alt_d = euclidean(COLOURS[i],m_256(result[1]))
                # print(d,i,euclidean(COLOURS[i],m_256(result[1])))
                if d < min_dist:
                    min_dist = d
                    result_colour = i
                if alt_d < alt_min_dist:
                    alt_min_dist = alt_d
                    alt_colour = i
            count = 0
            inventory = Inventory.objects.filter(user=self.request.user)
            for j in inventory:
                if j.entry.item.colour == result_colour and result[0] == j.item.type.name:
                    count += 1
            return Response({"type":result[0],
                             "colour":result_colour,
                             "alt_colour":alt_colour,
                             "count":count})