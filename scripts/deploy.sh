# deploy/deploy.sh
#!/bin/bash

# Charger la variable VENV_PATH depuis le fichier .env
export $(grep '^VENV_PATH=' .env)

# Arrêter les services
sudo systemctl stop gunicorn
# Arrêter Nginx
sudo systemctl stop nginx

# Mettre à jour le code
git pull origin main
# change to project directory 
cd myblog

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

sudo systemctl start gunicorn
sudo systemctl start nginx