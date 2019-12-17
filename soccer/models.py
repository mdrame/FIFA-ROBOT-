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

    # def get_absolute_url(self):
    #     """ Returns a fully-qualified path for a page (/my-new-wiki-page). """
    #     path_components = {'name': self.name}
    #     return reverse('wiki-details-page', kwargs=path_components)

    # def save(self, *args, **kwargs):
    #     """ Creates a URL safe slug automatically when a new a page is created. """
    #     if not self.pk:
    #         self.slug = slugify(self.title, allow_unicode=True)
    #
    #     # Call save on the superclass.
    #     return super(Team, self).save(*args, **kwargs)
