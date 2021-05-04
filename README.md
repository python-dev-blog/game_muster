# Game Muster

Тестовое приложение, отображающее список игр из IGDB API, созданное для демонстрации [подготовки django-приложения к деплойменту](https://www.youtube.com/watch?v=03egj6YEUFY)

## Quickstart

Run the following commands to bootstrap your environment:
    
    sudo apt egt update
    sudo apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim libpq-dev
    git clone https://github.com/python-dev-blog/game_muster
    cd game_muster
      
    python3 -m venv venv   
    source venv/bin/activate
    pip3 install -r requirements/dev.txt 

    cp .env.template .env
    while read file; do
       export "$file"
       done < .env

Run the app locally:

    python3 manage.py runserver 0.0.0.0:8000 --settings=game_muster.settings.dev

Run the app with gunicorn:

    gunicorn game_muster.wsgi -b 0.0.0.0:8000

### IGDB usage:

Get a list of games from IGDB API:
    
    python3 manage.py shell

    >>>> from game_catalog.utils.igdb_api import IgdbApi
    >>>> IgdbApi().get_games()

