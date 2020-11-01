from rest_framework import serializers
from raiment.models import UserProfile,Message,Conversation
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.fields import CurrentUserDefault


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
        fields = ('user',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data.get('user'))
        user.set_password(user.password)
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        token = Token.objects.create(user=user)
        token.save()
        return user_profile

