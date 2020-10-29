from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from raiment.models import UserProfile, Conversation,Message
from rest_framework import generics
from raiment.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
import json


class HelloView(APIView):
    def get(self, request):
        id = request.user.id
        content = {'message': id}
        return Response(content)


@authentication_classes([])
@permission_classes([])
class SignUp(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })


class MessageView(APIView):
    def post(self, request):
        author = request.user
        try:
            print(type(request.POST.get("receiver")))
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            return HttpResponse("Nope")
        try:
            c = Conversation.objects.get(user1__in=[author, receiver], user2__in=[author, receiver])
        except Conversation.DoesNotExist:
            c = Conversation.objects.create(user1=author, user2=receiver)

        message = Message.objects.create(author=author, txt=request.POST.get("txt"), conversation=c)
        return HttpResponse("Alright")

    def get(self,request):
        author = request.user
        try:
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            return HttpResponse("Nope")
        try:
            c = Conversation.objects.get(user1__in=[author, receiver], user2__in=[author, receiver])
        except Conversation.DoesNotExist:
            return HttpResponse("Nope")

        qs = Message.objects.filter(conversation=c)
        result = {"users":(author.username,receiver.username,),"messages":[]}
        for i in qs:
            result["messages"].append(
                {
                    "author":i.author.username,
                    "message":i.txt,
                    "date":str(i.date)
                })
        return JsonResponse(result)