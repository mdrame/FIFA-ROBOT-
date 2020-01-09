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

from datetime import datetime, timedelta, timezone
import os

import pytz

class HomePageView(ListView):
    """ Renders a list of all Teams. """
    model = Team

    def get_current_datetime_on_api_server(self):
        api_tz = pytz.timezone("Europe/London")

        london_time = datetime.now(tz=timezone.utc).astimezone(api_tz)
        return london_time

    def to_local_datetime(self, start_date):
        # Change this to your timezone
        local_tz = pytz.timezone("Europe/Rome")
        api_tz = pytz.timezone("Europe/London")

        dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        return api_tz.localize(dt).astimezone(local_tz)

    def footballprediction(self):
        # this is a datetime object with the timezone used by our api
        current_server_time = self.get_current_datetime_on_api_server()

        # obtaining the next day as python date object
        tomorrow = current_server_time.date() + timedelta(days=1)

        # today date
        today = current_server_time.date()


        url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/date/"+str(today)

        querystring = {"timezone":"Europe/London"}

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        matches = []

        if response.ok:
            json = response.json()

            data = json["api"]
            fixtures = data["fixtures"]

            for fixture in fixtures:
                match = {
                    "date": fixture["event_date"],
                    "league": fixture["league"]["name"],
                    "country": fixture["league"]["country"],
                    "round": fixture["round"],
                    "home_team": fixture["homeTeam"]["team_name"],
                    "away_team": fixture["awayTeam"]["team_name"],
                    "status": fixture["status"],
                    "venue": fixture["venue"],
                    "home_logo": fixture["homeTeam"]["logo"],
                    "away_logo": fixture["awayTeam"]["logo"],
                }
                matches.append(match)



        # print(response.text)

        return matches

    def football_data_api(self):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': '1e133e76dd1f4262a3c4a56dc713352b' }

        connection.request('GET', '/v2/teams/67/matches?status=FINISHED&limit=1', None, headers )
        response = json.loads(connection.getresponse().read().decode())

        return response

    def get(self, request):
        """ GET a list of Teams. """
        matches = self.footballprediction()
        # teams = ''
        # teams = self.football_data_api()
        print("__________________")
        print(matches)
        print("__________________")
        return render(request, 'index.html', {
          'matches': matches
        })


class DetailPageView(DetailView):
    """ Renders a single team. """
    model = Team

    def get(self, request, team_name):
        # olive = OliveOil.objects.get(pk=olive_id)
        team = team_name

        return render(request, 'detail.html', {'team': team_name})
