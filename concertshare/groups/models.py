from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    artists = models.ForeignKey(User.artists, on_delete=models.CASCADE)    

class Artist(models.Model):
    users = models.ManyToManyField(User)
    upcoming_count = models.IntegerField()
    id = models.IntegerField()
    url = models.CharField(maxlength=2083)
    thumb_url = models.CharField(maxlength=2083)
    image_url = models.CharField(maxlength=2083)
    facebook_page_url = models.CharField(maxlength=2083)

class Event(models.Model):
    offers = models.CharField(maxlength=2083)
    venue = models.CharField(maxlength=2083)
    datetime = models.DateField()
    on_sale_datetime = models.DateField()
    description = models.TextField()
    lineup = models.CharField(maxlength=300)
    id = models.IntegerField()
    artist_id = models.IntegerField()
    url = models.CharField(maxlength=2083)
