
from django.shortcuts import render

from game_catalog.utils.igdb_api import IgdbApi


def games(request):
    game_list = IgdbApi().get_games()
    return render(request, 'games.html', {'games': game_list})
