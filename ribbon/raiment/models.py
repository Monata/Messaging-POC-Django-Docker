from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Blocked(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blocker')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blocked')

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)





