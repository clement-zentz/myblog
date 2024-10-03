# Utiliser une image de base officielle Python
FROM python:latest

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de configuration et de dépendances
COPY ../requirements.txt .

# Affichez le contenu du répertoire après la copie pour le débogage
RUN ls -la /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]