import http.client
import json
import requests
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from soccer.models import Team, Match
from datetime import datetime, timedelta, timezone
import os
import pytz
from django.urls import reverse

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

    def get_fixtures_from_api(self):
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
                # date = self.to_local_datetime(fixture["event_date"])
                match = {
                    "fixtureId": fixture["fixture_id"],
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



    def get(self, request):
        """ GET a list of Teams. """
        matches = self.get_fixtures_from_api()

        return render(request, 'index.html', {
          'matches': matches
        })

    def post(self, request):
        pass

class DetailPageView(DetailView):
    """ Renders a single team. """
    model = Team


    def get_predictions_api(self, fixture_id):
        url = "https://api-football-v1.p.rapidapi.com/v2/predictions/"+str(fixture_id)

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }

        response = requests.request("GET", url, headers=headers)

        matchPrediction = {}

        if response.ok:
            json = response.json()

            data = json["api"]
            predictions = data["predictions"]

            for prediction in predictions:
                # date = self.to_local_datetime(fixture["event_date"])
                matchPrediction = {
                    "home_team": prediction["teams"]["home"]["team_name"],
                    "away_team": prediction["teams"]["away"]["team_name"],
                    "advice": prediction["advice"],
                    "home_winning_per": prediction["comparison"]["forme"]["home"],
                    "away_winning_per": prediction["comparison"]["forme"]["away"],

                    "home_win": prediction["winning_percent"]["home"],
                    "away_win": prediction["winning_percent"]["away"],
                    "draw_win": prediction["winning_percent"]["draws"],
                }

            headToHead = prediction["h2h"]

            allMatches = []
            for match in headToHead:
                game = {
                    "date": match["event_date"],
                    "home_team": match["homeTeam"]["team_name"],
                    "away_team": match["awayTeam"]["team_name"],
                    "home_goal": match["goalsHomeTeam"],
                    "away_goal": match["goalsAwayTeam"],
                    "status": match["status"],
                    "home_logo": match["homeTeam"]["logo"],
                    "away_logo": match["awayTeam"]["logo"],
                }
                allMatches.append(game)


        # print(response.text)

        return [matchPrediction, allMatches]

    def get(self, request, fixtureId):
        results = self.get_predictions_api(fixtureId)
        prediction = results[0]
        matches = results[1]
        home_logo = matches[0]["home_logo"]
        away_logo = matches[0]["away_logo"]
        return render(request, 'detail.html', {'prediction': prediction, 'matches': matches, "home_logo": home_logo, "away_logo": away_logo})

class MyAccountPageView(ListView):
    """ Renders a list of all Teams. """
    model = Match

    def get_queryset(self, user):
        """
        Excludes any questions that aren't published yet.
        """
        return Match.objects.filter(user=user)


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

    def get_fixtures_from_api(self, id):

        url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/"+str(id)

        querystring = {"timezone":"Europe/London"}

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        match = {}

        if response.ok:
            json = response.json()

            data = json["api"]
            fixturesList = data["fixtures"]

            for fixture in fixturesList:
                # date = self.to_local_datetime(fixture["event_date"])
                game = {
                    "fixtureId": fixture["fixture_id"],
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

        # print(response.text)

        return game


    def get(self, request):
        user_matches = self.get_queryset(request.user)
        print("___________")
        print(user_matches)
        print("___________")

        matches = []

        for a_match in user_matches:
            matches.append(self.get_fixtures_from_api(a_match.fixture_id))

        return render(request, 'myAccount.html', {
          'matches': matches
        })

    def post(self, request):
        pass

def saveMatch(request, fixtureId):

    match = Match()
    match.fixture_id = fixtureId
    match.user = request.user
    match.save()

#     # Always return an HttpResponseRedirect after successfully dealing
#     # with POST data. This prevents data from being posted twice if a
#     # user hits the Back button.
    return HttpResponseRedirect(reverse('soccer:myaccount'))

def deleteMatch(request, fixtureId):
    match = Match.objects.filter(fixture_id=fixtureId).delete()
    return HttpResponseRedirect(reverse('soccer:myaccount'))
