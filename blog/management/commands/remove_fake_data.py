from django.core.management.base import BaseCommand
from blog.models import Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Supprime toutes les données de l\'application de blog'

    def handle(self, *args, **kwargs):
        # Supprime toutes les instances des modèles
        User.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                'Toutes les données ont été supprimmées avec succès'
            )
        )