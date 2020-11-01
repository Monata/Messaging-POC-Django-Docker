from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
import logging
from raiment.models import Conversation, Message, Blocked
from rest_framework import generics
from raiment.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

logger = logging.getLogger('warnings')



class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            logger.warning("Invalid Login {}".format(request.data))
            return JsonResponse(
                {'error_message': "Invalid Login"})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        logger.warning('{} logged in'.format(user.username))
        return Response({'token': token.key})

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
        msg = "{} signed up".format(user.user.username)
        logger.warning(msg)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })


class MessageView(APIView):
    def post(self, request):
        author = request.user  # current_user
        try:
            receiver = User.objects.get(username=request.POST.get("receiver"))
        except User.DoesNotExist:
            msg = "User Doesn't Exist:MessageView:{}".format(author.username)
            logger.warning(msg)
            return JsonResponse({'error_message': "The user that you're trying to send a message to doesn't exist"})
        if receiver.username == author.username:
            msg = "{} tried to send a message to itself".format(author.username)
            logger.warning(msg)
            return JsonResponse({'error_message': "You can't send messages to yourself"})
        if Blocked.objects.filter(blocker=receiver, blocked=author).exists():
            msg = "{} tried to send a message to {} but is blocked".format(author.username, receiver.username)
            logger.warning(msg)
            return JsonResponse(
                {'error_message': "You can't send messages to " + author.username + " for you're blocked by that user"})

        try:
            c = Conversation.objects.get(user1__in=[author, receiver], user2__in=[author, receiver])
        except Conversation.DoesNotExist:
            c = Conversation.objects.create(user1=author, user2=receiver)

        message = Message.objects.create(author=author, txt=request.POST.get("txt"), conversation=c)
        msg = "{} sent a message to {}".format(author.username, receiver.username)
        logger.warning(msg)
        return JsonResponse({"from": author.username, "to": receiver.username, "txt": request.POST.get("txt")})

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
            msg = "User Doesn't Exist:BlockView:{}".format(author.username)
            logger.warning(msg)
            return JsonResponse({'error_message': "The user that you're trying to block doesn't exist"})
        if receiver.username == author.username:
            msg = "{} tried to block itself".format(author.username)
            logger.warning(msg)
            return JsonResponse({'error_message': "You can't block yourself"})
        try:
            Blocked.objects.get(blocker=author, blocked=receiver)
        except Blocked.DoesNotExist:
            Blocked.objects.create(blocker=author, blocked=receiver)
            msg = "{} blocked {}".format(author.username, receiver.username)
            logger.warning(msg)
            return JsonResponse({'blocker': author.username, 'blocked': receiver.username})
        msg = "{} tried blocking {} but blocked before".format(author.username, receiver.username)
        logger.warning(msg)
        return JsonResponse(
            {'error_message': "The user that you're trying to block has already been blocked by you"})

    def get(self, request):
        current_user = request.user
        qs = Blocked.objects.filter(blocker=current_user)
        result = {"blocker": current_user.username, "blocked_users": []}
        for i in qs:
            result["blocked_users"].append(i.blocked.username)
        return JsonResponse(result)
