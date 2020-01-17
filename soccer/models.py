from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
# from django.utils.text import slugify
# from django.contrib.auth.models import User


class Team(models.Model):
    """ Represents a single wiki page. """
    name = models.CharField(unique=True, help_text="Team name", max_length=1000)

    def __str__(self):
        return self.name


class Match(models.Model):
    """ represent single match """
    fixture_id = models.CharField(unique=True, help_text="fixture_id", max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.fixture_id
