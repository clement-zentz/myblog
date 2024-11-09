# scripts/deploy.sh
#!/bin/bash

# Charger la variable VENV_PATH depuis le fichier .env
export $(grep '^VENV_PATH=' .env)

# Arrêter les services
sudo systemctl stop gunicorn
# Arrêter Nginx
sudo systemctl stop nginx

# change directory to git repo 
cd ../
# Mettre à jour le code
git pull origin main

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# check if venv is activated
if [ $? -ne 0 ]
then
    echo "Virtual environment could not be activated."
    exit 1
fi

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

sudo systemctl restart gunicorn
sudo systemctl restart nginx