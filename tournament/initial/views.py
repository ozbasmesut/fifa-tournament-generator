from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .models import Season,Fixture,Club
from django.forms.models import model_to_dict

from random import choice

from .fixture_generator import Generator

def index(request):
    return HttpResponse("Hello, world. You're at the initial index.")

def list(request):
    # Load seasons for the list page
    seasons = Season.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'season_list.html',
        {'seasons': seasons}
    )

def detail(request, pk):
    # Load the season for the detail page
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    fixtures = Fixture.objects.filter(season_id = season.id)

    # Render list page with the documents and the form
    return render(
        request,
        'season_detail.html',
        {'season': season, 'fixtures': fixtures, 'teams': teams}
    )

class Match(object):
    homeTeam = ""
    awayTeam = ""
    # The class "constructor" - It's actually an initializer
    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam

# there could be type change like 'numberOfRounds'
def makefixture(request, pk):
    # Load the season for the detail page
    season = Season.objects.get(pk=pk)
    teams = season.getTeams().all()
    clubs = Club.objects.all()
    team_count = teams.count()

    generator = Generator(team_count)
    matches = generator.createFixtures()

    fixtures = []

    startWeek = 1
    clubList = clubs

    for match in matches:
        if match['week'] != startWeek:
            startWeek = match['week']
            clubList = clubs

        homeTeam = choice(clubList)
        clubList = clubList.exclude(pk=homeTeam.id)
        awayTeam = choice(clubList)
        clubList = clubList.exclude(pk=awayTeam.id)

        fixture = {
            "season_id": season.id,
            "week": match['week'],
            "home_team_id": teams[match['home'] - 1].id,
            "home_team_club": homeTeam.name,
            "away_team_id": teams[match['away'] - 1].id,
            "away_team_club": awayTeam.name,
        }
        fixtures.append(fixture)

    import json

    return HttpResponse(json.dumps(fixtures))