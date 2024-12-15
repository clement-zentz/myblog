#!/bin/bash
# transfer_srv_files_to_staging.sh

# exécuter ce script depuis le dossier "root" du projet

# Set the locale to handle special characters
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Chemin absolue vers le fichier .env
ENV_FILE_PATH=$(pwd)

echo $ENV_FILE_PATH

ENV_FILE_PATH+="/.env"

# Vérifier l'existence du fichier .env
if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Le fichier .env n'existe pas à l'emplacement spécifié : $ENV_FILE_PATH"
    exit 1
fi

# Enable automatic exporting of variable
set -a
# Source the environment file
source "$ENV_FILE_PATH"
# Disable automatic exporting of variables
set +a

# Vérifier que les variables sont définies
if [ -z "$STAGE_PORT" ] ||[ -z "$STAGE_USERNAME" ] || \
[ -z "$STAGE_IP_ADDRESS" ] || [ -z "$SSH_COMMANDS_PATH" ]; then
    echo "Une ou plusieurs variables d'environnement ne sont pas définies."
    exit 1
fi

scp -P $STAGE_PORT $GUNICORN_LOCAL_PATH \
    $STAGE_USERNAME@$STAGE_IP_ADDRESS:$GUNICORN_REMOTE_PATH

NEW_FILE_NAME=$STAGE_HTTPS_FILENAME
OLD_FILE_NAME=$STAGE_HTTP_FILENAME

scp -P $STAGE_PORT $NGINX_LOCAL_PATH/$NEW_FILE_NAME \
    $STAGE_USERNAME@$STAGE_IP_ADDRESS:$NGINX_REMOTE_PATH/$NEW_FILE_NAME

read -sp 'Enter sudo password: ' sudo_password
echo

# TODO add ssl certificate first

SSH_COMMANDS="
echo '$sudo_password' | sudo -S -v
sudo apt-get update 
sudo apt-get upgrade -y
sudo ln -s $NGINX_REMOTE_PATH/$NEW_FILE_NAME $NGINX_SITES_ENABLED_PATH/$NEW_FILE_NAME 
sudo rm $NGINX_SITES_ENABLED_PATH/$OLD_FILE_NAME
echo '$sudo_password' | sudo systemctl restart gunicorn 
echo '$sudo_password' | sudo systemctl restart nginx 
"

# exécute les commandes ssh
ssh -p $STAGE_PORT $STAGE_USERNAME@$STAGE_IP_ADDRESS "$SSH_COMMANDS"

# Vérifier le statut de la commande
if [ $? -eq 0 ]; then
    echo "Commandes exécutées avec succès."
else
    echo "Échec de l'exécution des commandes."
fi