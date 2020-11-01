from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User

from raiment.models import Conversation, Message, Blocked
from rest_framework import generics
from raiment.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view


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
        author = request.user  # current_user
        try:
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            return JsonResponse({'error_message': "The user that you're trying to send a message to doesn't exist"})
        if receiver.username == author.username:
            return JsonResponse({'error_message': "You can't send messages to yourself"})
        if Blocked.objects.filter(blocker=receiver, blocked=author).exists():
            return JsonResponse(
                {'error_message': "You can't send messages to " + author.username + " for you're blocked by that user"})

        try:
            c = Conversation.objects.get(user1__in=[author, receiver], user2__in=[author, receiver])
        except Conversation.DoesNotExist:
            c = Conversation.objects.create(user1=author, user2=receiver)

        message = Message.objects.create(author=author, txt=request.POST.get("txt"), conversation=c)
        return HttpResponse("Alright")

    def get(self, request):
        author = request.user
        try:
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            return HttpResponse("Nope")
        if receiver.username == author.username:
            return JsonResponse({'error_message': "You can't get messages from yourself"})
        try:
            c = Conversation.objects.get(user1__in=[author, receiver], user2__in=[author, receiver])
        except Conversation.DoesNotExist:
            return JsonResponse(
                {'error_message': "No messages has been found between " + author.username + "and " + receiver.username})

        qs = Message.objects.filter(conversation=c)
        result = {"users": (author.username, receiver.username,), "messages": []}
        for i in qs:
            result["messages"].append(
                {
                    "author": i.author.username,
                    "message": i.txt,
                    "date": str(i.date)
                })
        return JsonResponse(result)


class BlockView(APIView):
    def post(self, request):
        author = request.user
        try:
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            return JsonResponse({'error_message': "The user that you're trying to block doesn't exist"})
        if receiver.username == author.username:
            return JsonResponse({'error_message': "You can't block yourself"})
        try:
            c = Blocked.objects.create(blocker=author, blocked=receiver)
        except Conversation.DoesNotExist:
            return JsonResponse(
                {'error_message': "The user that you're trying to block has already been blocked by you"})

        return JsonResponse({'blocker': author.username, 'blocked': receiver.username})

    def get(self, request):
        current_user = request.user
        qs = Blocked.objects.filter(blocker=current_user)
        result = {"blocker": current_user.username, "blocked_users": []}
        for i in qs:
            result["blocked_users"].append(i.blocked.username)
        return JsonResponse(result)


class TestView(APIView):
    pass
