
ORtGX#2xkxtmwDs

sudo service supervisor  stop

sudo service supervisor  start

python3 -m venv config

source config/env/bin/activate
 
cd config

python manage.py makemigrations