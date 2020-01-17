import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Team, Match


class MatchModelTest(TestCase):

    def test_saving_match(self):
        pass
