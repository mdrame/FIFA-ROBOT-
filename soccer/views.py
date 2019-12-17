import requests
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
# from django.contrib.auth import logout
# from .forms import PageForm
from django.http import HttpResponseRedirect

from soccer.models import Team


class HomePageView(ListView):
    """ Renders a list of all Pages. """
    model = Team

    def getFederations(self):

        # url = "https://football-prediction-api.p.rapidapi.com/api/v2/performance-stats"
        url = "https://football-prediction-api.p.rapidapi.com/api/v2/list-federations"

        querystring = {"market":"classic"}

        headers = {
            'x-rapidapi-host': "football-prediction-api.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }

        # response = requests.request("GET", url, headers=headers, params=querystring)
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.text


        return data

    def get(self, request):
        """ GET a list of Teams. """
        # teams = self.get_queryset().all()

        teams = self.getFederations()
        print("__________________")
        print(teams)
        print("__________________")
        return render(request, 'index.html', {
          'teams': teams
        })
