# Game Muster

Тестовое приложение, отображающее список игр из IGDB API, созданное для демонстрации [подготовки django-приложения к деплойменту](https://www.youtube.com/watch?v=03egj6YEUFY)

## Quickstart

Run the following commands to bootstrap your environment:
    
    sudo apt get update
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
    
Collect static files:

    python3 manage.py collectstatic --settings=game_muster.settings.prod
    

### IGDB usage:

Get a list of games from IGDB API:
    
    python3 manage.py shell

    >>>> from game_catalog.utils.igdb_api import IgdbApi
    >>>> IgdbApi().get_games()
    >>>> 


### Setup NGINX:

    sudo vim /etc/nginx/sites-enabled/default:
    
Config file:

    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            location /static/ {
                alias /home/user/game_muster/static/; 
            }

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_redirect off;
                add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';
                add_header Access-Control-Allow-Origin *;
            }
    }
    
Restart NGINX:
    
    sudo service nginx restart
    
    
### Setup Supervisor:

    cd /etc/supervisor/conf.d/
    sudo vim game_muster.conf
    
Config file:
    
    [program:game_muster]
    command = /home/user/game_muster/venv/bin/gunicorn game_muster.wsgi  -b 0.0.0.0:8000 -w 4 --timeout 90
    autostart=true
    autorestart=true
    directory=/home/user/game_muster 
    stderr_logfile=/var/log/game_muster.err.log
    stdout_logfile=/var/log/game_muster.out.log
    
Update supervisor with the new process:
    
    sudo supervisorctl reread
    sudo supervisorctl update
    
To restart the process after the code updates run:

    sudo supervisorctl restart game_muster

    
   

