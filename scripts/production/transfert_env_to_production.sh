#!/bin/bash
# transfert_env_to_stage.sh

# exécuter ce script depuis le dossier "root" du projet

# Chemin absolue vers le fichier .env
ENV_FILE_PATH=$(pwd)

ENV_FILE_PATH+="/.env"

# Vérifier l'existence du fichier .env
if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Le fichier .env n'existe pas à l'emplacement spécifié : $ENV_FILE_PATH"
    exit 1
fi

# Charger les variables d'environnement depuis le fichier .env
set -a
source "$ENV_FILE_PATH"
set +a

# Vérifier que les variables sont définies
if [ -z "$PROD_PORT" ] || [ -z "$PROD_ENV_LOCAL_PATH" ] || \
[ -z "$PROD_USERNAME" ] || [ -z "$PROD_IP_ADDRESS" ] || \
[ -z "$PROD_ENV_REMOTE_PATH" ]; then
    echo "Une ou plusieurs variables d'environnement ne sont pas définies."
    exit 1
fi

# transfert env file to vps
scp -P $PROD_PORT $PROD_ENV_LOCAL_PATH \
    $PROD_USERNAME@$PROD_IP_ADDRESS:$PROD_ENV_REMOTE_PATH

# Vérifier le statut de la commande
if [ $? -eq 0 ]; then
    echo "Commandes exécutées avec succès."
else
    echo "Échec de l'exécution des commandes."
fi