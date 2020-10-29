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
        userProfile = UserProfile.objects.create(user=user)
        userProfile.save()
        token = Token.objects.create(user=user)
        token.save()
        return userProfile

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = ('receiver','txt')
#
#     def create(self, validated_data):
#         author = self.context.get('request').user
#         try:
#             receiver = User.objects.get(username=validated_data['receiver'])
#         except User.DoesNotExist:
#             return None
#         try:
#             c = Conversation.objects.get(user1__in=[author,receiver],user2__in=[author,receiver])
#         except Conversation.DoesNotExist:
#             c = Conversation.objects.create(user1=author,user2=receiver)
#
#         message = Message.objects.create(author=author,txt=validated_data['txt'],conversation=c)
#         return message
