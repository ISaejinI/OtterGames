from django.core.management.base import BaseCommand
from tournois.models import Loutre
import random

class Command(BaseCommand):
    help = 'Génère 8 loutres aléatoires'

    def handle(self, *args, **options):
        prenoms = ['Loutre1', 'Loutre2', 'Loutre3', 'Loutre4', 'Loutre5', 'Loutre6', 'Loutre7', 'Loutre8']
        noms = ['Rapide', 'Féroce', 'Rusée', 'Maligne', 'Gourmande', 'Nerveuse', 'Curieuse', 'Agile']
        villages = ['Rivière Claire', 'Bois Tranquille', 'Lac Mystère', 'Baie Joyeuse']

        for i in range(8):
            loutre = Loutre.objects.create(
                nom=noms[i],
                prenom=prenoms[i],
                age=random.randint(2, 10),
                village=random.choice(villages),
                poids=round(random.uniform(5.0, 15.0), 1),
                taille=round(random.uniform(50.0, 100.0), 1),
                description=f'Loutre n°{i+1}, prête au combat!'
            )
            self.stdout.write(self.style.SUCCESS(f'Loutre créée : {loutre.prenom} {loutre.nom}'))

        self.stdout.write(self.style.SUCCESS('✅ 8 loutres ajoutées avec succès.'))
