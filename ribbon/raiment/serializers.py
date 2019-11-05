from rest_framework import serializers
from raiment.models import Clothing

class ClothingSerializer(serializers.ModelSerializer):
    #to convert django models to JSON
    class Meta:
        model = Clothing
        fields = '__all__' #('type','color_tag','brand')

