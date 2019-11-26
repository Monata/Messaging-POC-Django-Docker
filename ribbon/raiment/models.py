from django.db import models


class Item(models.Model):
    # Class to store information about our clothing
    size = models.CharField(max_length=8)
    colour = models.CharField(max_length=32)
    price = models.FloatField()
    brand = models.CharField(max_length=50)
    material = models.CharField(max_length=32)
    image_link = models.URLField()


class Entry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    wearcount = models.PositiveIntegerField()
    count = models.PositiveIntegerField()


class Folder(models.Model):
    created = models.DateTimeField()


class FolderHas(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class Packlist(models.Model):
    date = models.DateField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class CalendarDay(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    day = models.DateField()


class User(models.Model):
    # Can be subsituted by models.User
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    size_letter = models.CharField(max_length=8)
    size_shoe = models.PositiveSmallIntegerField()
    size_pants = models.PositiveSmallIntegerField()


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(CalendarDay, on_delete=models.CASCADE)


class FolderInventory():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)


class PacklistInventory():
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

