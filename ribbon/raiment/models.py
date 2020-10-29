from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from ribbon.settings import COLOURS

colour_choices = [(i,i) for i in COLOURS]

class ItemType(models.Model):
    # Class to store type
    name = models.CharField(max_length=32)

class Item(models.Model):
    # Class to store information about our clothing
    colour = models.CharField(null = True,max_length=32,choices = colour_choices)
    image_link = models.URLField()
    material = models.CharField(max_length=32)
    price = models.FloatField()
    size = models.CharField(max_length=8)
    brand = models.CharField(max_length=50)
    weather = models.CharField(null = True,max_length=32,choices=[('sunny','sunny'),('cloudy','cloudy'),('rainy','rainy')])
    type = models.ForeignKey(ItemType, on_delete=models.SET_NULL,null=True)





class Entry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    wearcount = models.PositiveIntegerField()
    count = models.PositiveIntegerField()


class Folder(models.Model):
    # Creates a folder with the current time, the creation time uses server's creation time which is a bit problematic
    created = models.DateTimeField(auto_now_add=True)


class FolderHas(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class Packlist(models.Model):
    name = models.CharField(max_length=256,default="Nameless Packlist")
    date = models.DateField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class CalendarDay(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    day = models.DateField()



class UserProfile(models.Model):
    # Can be subsituted by models.User

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)
    size_letter = models.CharField(max_length=8,blank=True,null=True)
    size_shoe = models.PositiveSmallIntegerField(blank=True,null=True)
    size_pants = models.PositiveSmallIntegerField(blank=True,null=True)

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(CalendarDay, on_delete=models.CASCADE)


class FolderInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class PacklistInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    packlist = models.ForeignKey(Packlist, on_delete=models.CASCADE)


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)


class Brand(models.Model):
    name = models.CharField(max_length=32)
    website = models.URLField()


class Catalogue(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    type = models.CharField(max_length=32)


class CatalogueHas(models.Model):
    catalogue = models.ForeignKey(Catalogue,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

