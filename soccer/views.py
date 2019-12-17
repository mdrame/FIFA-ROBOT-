import http.client
import json
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
    """ Renders a list of all Teams. """
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

    def football_data_api(self):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': '1e133e76dd1f4262a3c4a56dc713352b' }

        connection.request('GET', '/v2/teams/67/matches?status=FINISHED&limit=1', None, headers )
        response = json.loads(connection.getresponse().read().decode())

        return response

    def get(self, request):
        """ GET a list of Teams. """
        # teams = self.get_queryset().all()

        teams = self.football_data_api()
        print("__________________")
        print(teams)
        print("__________________")
        return render(request, 'index.html', {
          'teams': teams
        })


class DetailPageView(DetailView):
    """ Renders a single team. """
    model = Team

    def get(self, request, team_name):
        # olive = OliveOil.objects.get(pk=olive_id)
        team = team_name

        return render(request, 'detail.html', {'team': team_name})
