from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from blog.models import Category

class Command(BaseCommand):
    help = 'Supprime toutes les données de l\'application de blog'
    # use transaction to rollback errors
    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            # Supprime toutes les instances des modèles
            users_to_delete = User.objects.filter(
                is_staff=False,
                is_superuser=False)
            
            users_to_delete.delete()

            categories_to_delete = Category.objects.exclude(
                id=1000
            )
            
            categories_to_delete.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    'Toutes les données ont été supprimmées avec succès'
                )
            )
        except Exception as e:
            transaction.set_rollback(True)
            self.stdout.write(self.style.ERROR(f'Error removing fake data: {e}'))