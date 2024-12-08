# scripts/deploy.sh
#!/bin/bash

# exécuter ce script depuis le dossier root du projet

# Charger la variable VENV_PATH depuis le fichier .env
export $(grep '^VENV_PATH=' .env | xargs)

# Mettre à jour le code
git pull origin main

# Activer l'environnement virtuel
source $VENV_PATH

# check if venv is activated
if [ $? -ne 0 ]
then
    echo "Virtual environment could not be activated."
    exit 1
fi

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python3 manage.py migrate

# Collecter les fichiers statiques
python3 manage.py collectstatic --noinput

# redémarrer gunicorn et nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "Mise à jour et redémarrage terminés."