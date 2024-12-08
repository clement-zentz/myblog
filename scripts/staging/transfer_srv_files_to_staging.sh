#!/bin/bash
# transfer_srv_files_to_staging.sh

# exécuter ce script depuis le dossier "root" du projet

# Chemin absolue vers le fichier .env
ENV_FILE_PATH=$(pwd)

ENV_FILE_PATH+="/.env"

# Vérifier l'existence du fichier .env
if [ ! -f "$ENV_FILE" ]; then
    echo "Le fichier .env n'existe pas à l'emplacement spécifié : $ENV_FILE"
    exit 1
fi

# Charger les variables d'environnement depuis le fichier .env
set -a
source "$ENV_FILE"
set +a

# Vérifier que les variables sont définies
if [ -z "$STAGE_PORT" ] ||[ -z "$STAGE_USERNAME" ] || \
[ -z "$STAGE_IP_ADDRESS" ] || [ -z "$SSH_COMMANDS_PATH" ]; then
    echo "Une ou plusieurs variables d'environnement ne sont pas définies."
    exit 1
fi

scp -P $STAGE_PORT $STAGE_GUNICORN_LOCAL_PATH \
    $STAGE_USERNAME@$STAGE_IP_ADDRESS:$STAGE_GUNICORN_REMOTE_PATH

scp -P $STAGE_PORT $STAGE_NGINX_LOCAL_PATH \
    $STAGE_USERNAME@$STAGE_IP_ADDRESS:$STAGE_NGINX_REMOTE_PATH

# récupére les commandes ssh dans la variable REMOTE_COMMANDS
set -a
source $SSH_COMMANDS_PATH
set +a

# exécute les commandes ssh
ssh -p $STAGE_PORT $STAGE_USERNAME@$STAGE_IP_ADDRESS "$REMOTE_COMMANDS"

# Vérifier le statut de la commande
if [ $? -eq 0 ]; then
    echo "Commandes exécutées avec succès."
else
    echo "Échec de l'exécution des commandes."
fi