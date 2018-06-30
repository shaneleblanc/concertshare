from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Your Real Name"), blank=True, max_length=255)
    cities = models.CharField(_("Cities"), default="San Francisco", max_length=255)
    artists = models.TextField(_("Artists"), blank=True, max_length=25500)
    date_range = models.CharField(_("Date Range"), blank=True, max_length=48)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Group(models.Model):
    name = models.CharField(_("Name of Group"), blank=True, max_length=255)
    cities = models.CharField(_("Cities"), default="San Francisco", max_length=255)
    artists = models.TextField(_("Artists"), blank=True, max_length=25500)
    date_range = models.CharField(_("Date Range"), blank=True, max_length=48)
    users = models.ManyToManyField(User)
    

    @classmethod
    def create(cls, name):
        group = cls(name=name)
        # do something with the book
        return group
