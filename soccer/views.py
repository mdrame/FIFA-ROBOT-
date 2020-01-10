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

    # load current time
    def get_current_datetime_on_api_server(self):
        api_tz = pytz.timezone("America/Los_Angeles")
        # Los Angeles local time
        la_time = datetime.now(tz=timezone.utc).astimezone(api_tz)
        return la_time

    # convert time to local time
    def to_local_datetime(self, start_date):
        # Change this to your timezone
        local_tz = pytz.timezone("America/Los_Angeles")
        api_tz = pytz.timezone("Europe/London")

        dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        return api_tz.localize(dt).astimezone(local_tz)

    def get_fixtures_from_api(self):
        # this is a datetime object with the timezone used by our api
        current_server_time = self.get_current_datetime_on_api_server()
        # obtaining the next day as python date object
        tomorrow = current_server_time.date() + timedelta(days=1)
        # obtaining today's date
        today = current_server_time.date()

        # api link address
        url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/date/"+str(today)
        # query string
        querystring = {"timezone":"America/Los_Angeles"}
        # API credentials
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }
        # API response with results
        response = requests.request("GET", url, headers=headers, params=querystring)

        matches = [] # will store all matches from API

        if response.ok: # check response
            json = response.json() # get json data
            # obtain data from json
            data = json["api"] #type dict
            fixtures = data["fixtures"] #type array
            # loop over matches
            for fixture in fixtures:
                # convert time
                dateStr = fixture["event_date"]
                date  = datetime.strptime(dateStr[0:16], "%Y-%m-%dT%H:%M")
                # load single match data
                match = {
                    "fixtureId": fixture["fixture_id"],
                    "date": date,
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
                # add match to list
                matches.append(match)

        return matches



    def get(self, request):
        """ GET a list of Teams from API"""
        matches = self.get_fixtures_from_api()

        return render(request, 'index.html', {
          'matches': matches
        })


class DetailPageView(DetailView):
    """ Renders a single team. """
    model = Team

    # this function handles prediction call
    def get_predictions_api(self, fixture_id): # fixture_id is used to query from API
        # API link with id
        url = "https://api-football-v1.p.rapidapi.com/v2/predictions/"+str(fixture_id)
        # API credentials
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }
        #API response
        response = requests.request("GET", url, headers=headers)

        matchPrediction = {} # will store all prediction from API

        if response.ok:
            json = response.json() # get json data from response
            data = json["api"] # Dict type
            predictions = data["predictions"] # list type
            for prediction in predictions: # loop predictions
                # Obtain necessary data
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

            # next obtain all h2h matches
            headToHead = prediction["h2h"] # list type
            allMatches = [] # will store all matches

            for match in headToHead: #loop over matches
                # convert time
                dateStr = match["event_date"]
                date  = datetime.strptime(dateStr[0:16], "%Y-%m-%dT%H:%M")
                # Obtain necessary from api
                game = {
                    "date": date,
                    "home_team": match["homeTeam"]["team_name"],
                    "away_team": match["awayTeam"]["team_name"],
                    "home_goal": match["goalsHomeTeam"],
                    "away_goal": match["goalsAwayTeam"],
                    "status": match["status"],
                    "home_logo": match["homeTeam"]["logo"],
                    "away_logo": match["awayTeam"]["logo"],
                }
                # add single match to list
                allMatches.append(game)
        # return an array with both predictions and all matches
        return [matchPrediction, allMatches]

    def get(self, request, fixtureId):
        results = self.get_predictions_api(fixtureId) # return a list of matches and predictions
        # seperate matches and predictions
        prediction = results[0]
        matches = results[1]
        # obtain logos
        home_logo = matches[0]["home_logo"]
        away_logo = matches[0]["away_logo"]
        # render detail page
        return render(request, 'detail.html', {'prediction': prediction, 'matches': matches, "home_logo": home_logo, "away_logo": away_logo})

# This class will displays a specific user activities and more actions
class MyAccountPageView(ListView):
    """ Renders a list of all matches. """
    model = Match

    def get_queryset(self, user):
        """
        gets all matches for specific user
        """
        return Match.objects.filter(user=user)


    # get current time
    def get_current_datetime_on_api_server(self):
        api_tz = pytz.timezone("America/Los_Angeles")

        la_time = datetime.now(tz=timezone.utc).astimezone(api_tz)
        return la_time
    # convert time to local time
    def to_local_datetime(self, start_date):
        # Change this to your timezone
        local_tz = pytz.timezone("America/Los_Angeles")
        api_tz = pytz.timezone("Europe/London")

        dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        return api_tz.localize(dt).astimezone(local_tz)
    # make api call with id
    def get_fixtures_from_api(self, id):

        url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/id/"+str(id)

        querystring = {"timezone":"America/Los_Angeles"}

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
                dateStr = fixture["event_date"]
                date  = datetime.strptime(dateStr[0:16], "%Y-%m-%dT%H:%M")

                game = {
                    "fixtureId": fixture["fixture_id"],
                    "date": date,
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
        # will store all matches for specific user
        matches = []
        # loop over user mathes and make api call
        for a_match in user_matches:
            # append returned result to list of matches for a specific user
            matches.append(self.get_fixtures_from_api(a_match.fixture_id))

        return render(request, 'myAccount.html', {
          'matches': matches
        })


# save a single match for a specific user
def saveMatch(request, fixtureId):
    match = Match() # create an instance
    match.fixture_id = fixtureId # store fixture id
    match.user = request.user # store user
    match.save() # save match
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('soccer:myaccount'))


# delete a single match
def deleteMatch(request, fixtureId):
    # retrieve match from django and delete it
    match = Match.objects.filter(fixture_id=fixtureId).delete()
    return HttpResponseRedirect(reverse('soccer:myaccount'))
