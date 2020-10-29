from rest_framework import serializers
from raiment.models import Item,Packlist,Folder,FolderHas,UserProfile,ItemType,PacklistInventory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.fields import CurrentUserDefault


class ItemSerializer(serializers.ModelSerializer):
    # to convert django models to JSON
    class Meta:
        model = Item
        fields = '__all__'  # ('type','color_tag','brand')


class ItemTypeSerializer(serializers.ModelSerializer):
    # to convert django models to JSON
    class Meta:
        model = ItemType
        fields = '__all__'  # ('type','color_tag','brand')



class FolderHasSerializer(serializers.ModelSerializer):
    # to convert django models to JSON
    class Meta:
        model = FolderHas
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'


class PacklistSerializer(serializers.ModelSerializer):
    # to convert django models to JSON
    id = serializers.ReadOnlyField()

    class Meta:
        model = Packlist
        fields = ('id','name','date')

    def create(self,validated_data):
        folder = Folder.objects.create()
        p = Packlist.objects.create(name=validated_data.get('name'),folder=folder,date=validated_data.get('date'))
        request = self.context.get('request')
        u = request.user
        PacklistInventory.objects.create(user=u,packlist=p)
        return p



class hUserSerializer(serializers.ModelSerializer):
    # to convert django models to JSON

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    user = hUserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user','size_letter','size_shoe','size_pants')

    def create(self, validated_data):
        user = User.objects.create(**validated_data.get('user'))
        user.set_password(user.password)
        size_l = validated_data.get('size_letter')
        size_s = validated_data.get('size_shoe')
        size_p = validated_data.get('size_pants')
        user.save()
        userProfile = UserProfile.objects.create(user=user,size_letter=size_l, size_shoe=size_s,size_pants=size_p)
        userProfile.save()
        token = Token.objects.create(user=user)
        token.save()
        return userProfile
