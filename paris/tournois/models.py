from django.db import models
from loginUser.models import customUser

# Loutres participantes
class Loutre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField()
    village = models.CharField(max_length=100)
    poids = models.FloatField(help_text="Poids en kg")
    taille = models.FloatField(help_text="Taille en cm")
    description = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# Tournoi de loutres
class Tournoi(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    heure_lancement = models.DateTimeField()

    def __str__(self):
        return self.nom


# Match dans un tournoi
class Match(models.Model):
    tournoi = models.ForeignKey(Tournoi, related_name='matchs', on_delete=models.CASCADE)
    niveau = models.IntegerField(help_text="Niveau dans l'arbre, ex : 3 pour quarts, 2 demi, 1 finale")
    numero_match = models.IntegerField(help_text="Numéro du match dans le niveau")
    loutre1 = models.ForeignKey(Loutre, related_name='matchs_loutre1', on_delete=models.SET_NULL, null=True)
    loutre2 = models.ForeignKey(Loutre, related_name='matchs_loutre2', on_delete=models.SET_NULL, null=True)
    vainqueur = models.ForeignKey(Loutre, related_name='matchs_gagnes', on_delete=models.SET_NULL, null=True, blank=True)
    heure_lancement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tournoi.nom} - Niveau {self.niveau} - Match {self.numero_match}"


# Paris des utilisateurs (simplifié sans user)
class Pari(models.Model):
    user = models.ForeignKey(customUser, related_name='userId', on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name='paris', on_delete=models.CASCADE)
    loutre_misee = models.ForeignKey(Loutre, on_delete=models.CASCADE)
    resultat = models.BooleanField(null=True, blank=True, help_text="True = gagné, False = perdu, Null = pas encore terminé")

    def __str__(self):
        return f"{self.pseudo} a parié sur {self.loutre_misee} (Match {self.match.id})"
