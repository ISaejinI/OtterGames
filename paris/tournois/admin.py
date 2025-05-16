from django.contrib import admin
from django.contrib import messages
from django import forms
from .models import Loutre, Tournoi, Match, Pari
from django.db.models import Max
from datetime import timedelta
import random
import math


class TournoiAdminForm(forms.ModelForm): # class qui hérite de modelForm
    nb_participants = forms.ChoiceField( # champs personnalisé avec liste déroulante
        choices=[(8, '8'), (16, '16')],
        label='Nombre de participants',
        initial=8,
        help_text='Nombre de loutres participantes (doit être une puissance de 2)',
        required=False
    )

    class Meta:
        model = Tournoi # le formulaire est lié à tournoi
        fields = '__all__' # tout les champs de tournoi vont être repris


@admin.register(Tournoi)
class TournoiAdmin(admin.ModelAdmin): # utilise tournoiAdmin comme formulaire
    form = TournoiAdminForm
    list_display = ('nom', 'categorie', 'heure_lancement')
    # inlines = []

    def save_model(self, request, obj, form, change): # quand enregistrer ça fait la méthode (request -> la requêtre http de django, obj -> l'objet du tournoi qui vient d'être save, form -> c'est le formulaire, change -> si True c'est une modif sinon une création)
        super().save_model(request, obj, form, change) # ça enregistre l'objet j'ai pas trop bien compris

        if not change:  # Si c'est une création de tournoi
            nb_participants = int(form.cleaned_data.get('nb_participants') or 8) # récupère le nombre de participants que l'on a renseigné dans le formulaire
            self._creer_arbre_matches(request, obj, nb_participants) # on appelle la méthode pour créer un arbre de matches
            self._propager_vainqueurs(obj) # on appelle la méthode pour créer un arbre de matches

    def _creer_arbre_matches(self, request, tournoi, nb_participants): # méthode pour créer l'arbre des matches
        loutres = list(Loutre.objects.all()) # récupère toutes les loutres de la base de donnés et la transforme en list python
        if len(loutres) < nb_participants: # si il y a pas assez de loutre dans la bdd on envoie un message d'erreur
            self.message_user(request, "Pas assez de loutres pour ce tournoi.", level='error')
            return

        participants = random.sample(loutres, nb_participants) # sample prend en arguments, une population (ici notre liste), et un nombre k qui est notre nombre de personnes qu'on veut de la popupaltion (8 par exemple)
        nb_niveaux = int(math.log2(len(participants))) # calcul le nombre de niveau total qu'il y aura dans l'abrbre par rapport au nombre de participants
        matchs_par_niveau = len(participants) // 2 # calcul le nombre de match au niveau acutel
        heure_depart = tournoi.heure_lancement

        for niveau in range(nb_niveaux, 0, -1): # la boucle démarre au nombre niveaux maximum et descend de -1 par tour jusqu'à arriver à 0
            if niveau != nb_niveaux:
                heure_depart += timedelta(minutes=3)
            for i in range(matchs_par_niveau): # la boucle se stop quand tout les match du niveau sont créé
                if niveau == nb_niveaux: # la première fois on est au niveau 3 (pour 8 participants), c'est donc le même chiffre que le nombre de niveau total (3)
                    loutre1 = participants[i * 2] # 0, 2, 4 ,6
                    loutre2 = participants[i * 2 + 1] # 1, 3, 5, 7
                else: # après une boucle on a plus le même niveau actuel que celui total, car le niveau actuel est 2 et le total 3
                    loutre1 = None
                    loutre2 = None

                Match.objects.create( # créé le match dans la bdd
                    tournoi=tournoi,
                    niveau=niveau,
                    numero_match=i + 1,
                    loutre1=loutre1,
                    loutre2=loutre2,
                    heure_lancement=heure_depart
                )

                heure_depart += timedelta(minutes=1)

            matchs_par_niveau //= 2 # on divise le nombre de match par deux à chaque niveau
            
    def _propager_vainqueurs(self, tournoi):
        nb_niveaux = Match.objects.filter(tournoi=tournoi).aggregate(max_niveau=Max('niveau'))['max_niveau'] # cherche tout les matchs du tournois et trouve la profondeur max (exemple : 3)

        for niveau in range(nb_niveaux, 0, -1):
            matchs = Match.objects.filter(tournoi=tournoi, niveau=niveau).order_by('numero_match') # cherche tout les matchs de ce tournoi qui sont au même niveau (exemple: 3 ou 2)

            for match in matchs: # on passe sur chaque match
                if match.loutre1 and match.loutre2: # si il y a bien les 2 loutres dans le match (pas vide)
                    vainqueur = random.choice([match.loutre1, match.loutre2]) # prend une loutre aléatoriement
                    match.vainqueur = vainqueur
                    match.save() # sauvegarde dans la bdd
                else:
                    continue

                if niveau > 1: # si ce n'est pas la final
                    numero_match_suivant = (match.numero_match + 1) // 2 # division entière les match 3-1 et 3-2 vont dans le match 2-1 etc... pour les autres
                    match_suivant = Match.objects.get( # récupère le match qui va accueillir le vainqueur
                        tournoi=tournoi,
                        niveau=niveau - 1, # descend d'un niveau
                        numero_match=numero_match_suivant # met le nouveau numero de match pour trouver le bon
                    )

                    if not match_suivant.loutre1: # si il n'y a pas déjà au moins une loutre dans le prochain match
                        match_suivant.loutre1 = vainqueur # on la rajoute dans la loutre1 du prochain match
                    elif not match_suivant.loutre2: # sinon si il n'y a pas déjà une deuxième loutre dans le prochain match
                        match_suivant.loutre2 = vainqueur # on la rajoute dans la loutre2 du prochain match

                    match_suivant.save() # on sauvegarde le match avec ses nouvelles loutre qui vont s'affronter

@admin.register(Loutre)
class LoutreAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'village', 'age', 'poids', 'taille')
    search_fields = ('nom', 'prenom', 'village')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('tournoi', 'niveau', 'numero_match', 'loutre1', 'loutre2', 'vainqueur','heure_lancement')
    list_filter = ('tournoi', 'niveau', 'heure_lancement')
    search_fields = ('tournoi__nom',)


@admin.register(Pari)
class PariAdmin(admin.ModelAdmin):
    list_display = ('match', 'loutre_misee', 'resultat')
    list_filter = ('resultat', 'match__tournoi')
    search_fields = ('match__id',)
