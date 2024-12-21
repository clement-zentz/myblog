# ssl_autosign_cert.sh

# execute this script with an admin prompt

ENV_FILE_PATH=$(pwd)
# echo $ENV_FILE_PATH
ENV_FILE_PATH+="/.env"

# Vérifier l'existence du fichier .env
if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Le fichier .env n'existe pas à l'emplacement spécifié : $ENV_FILE_PATH"
    exit 1
fi

# get env variables
set -a
source "$ENV_FILE_PATH"
set +a

# Vérifier que les variables sont définies
if [ -z "$STAGE_PORT" ] ||[ -z "$STAGE_USERNAME" ] || \
[ -z "$STAGE_IP_ADDRESS" ] || [ -z "$COUNTRY" ] || \
[ -z "$STATE" ] || [ -z "$CITY" ] || [ -z "$ORGANIZATION" ] || \
[ -z "$COMMON_NAME" ] || [ -z "$HOSTS_FILE_PATH" ]; then
    echo "Une ou plusieurs variables d'environnement ne sont pas définies."
    exit 1
fi

IP_AND_DOMAIN="$STAGE_IP_ADDRESS $COMMON_NAME"

# on windows host machine for https domain
# echo "# Added by ssl_autosign_cert.sh" >> $HOSTS_FILE_PATH
# echo $IP_AND_DOMAIN >> $HOSTS_FILE_PATH
# echo "# End of ssl_autosign_cert.sh section." >> $HOSTS_FILE_PATH

read -sp 'Enter sudo password: ' sudo_password
echo

SSH_COMMANDS=$(cat <<EOF
echo '$sudo_password' | sudo -S -v
echo '$sudo_password' | sudo mkdir $SSL_PATH
cd $SSL_PATH
echo '$sudo_password' | sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx-selfsigned.key -out nginx-selfsigned.crt \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/CN=$COMMON_NAME"
EOF
)

# exécute les commandes ssh
ssh -p $STAGE_PORT $STAGE_USERNAME@$STAGE_IP_ADDRESS "$SSH_COMMANDS"