import json
import os

import requests
from game_muster.settings import base as settings


class IgdbApi:
    MAIN_FIELDS = ['name', 'screenshots.url', 'aggregated_rating']

    FIELDS = ['name', 'screenshots.url', 'summary', 'release_dates.date', 'rating', 'aggregated_rating',
              'genres.name', 'platforms.abbreviation', 'rating_count', 'tags', 'updated_at',
              'aggregated_rating_count']

    def __init__(self):
        self.__api_url = settings.IGDB_API_URL
        self.__query_header = {'Client-ID': settings.env('IGDB_CLIENT_ID'),
                               'Authorization': settings.env('IGDB_AUTH_KEY')}

    def get_games(self, limit=settings.RECORDS_LIMIT):
        url = self.__api_url + "games/"
        data = f"fields {','.join(self.MAIN_FIELDS)}; sort popularity desc; limit {limit};"
        response = requests.post(url, headers=self.__query_header, data=data)

        if response.status_code is settings.SUCCESS_STATUS:
            games = json.loads(response.text)
            for game in games:
                if 'screenshots' in game.keys():
                    game['screenshot_url'] = game['screenshots'][0]['url'].replace('t_thumb', 't_screenshot_huge')
            return games
        else:
            return None
