from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Tournoi, Loutre, Pari
from django.utils import timezone
import datetime

def allmatchs_page(request):
    matchs = Match.objects.all()

    return render(request, 'allmatchs.html', {'matchs': matchs})

def alltournois_page(request):
    tournois = Tournoi.objects.all()

    return render(request, 'alltournois.html', {'tournois': tournois})

def tournoi_page(request, tournoi_id):
    tournoi = Tournoi.objects.get(pk = tournoi_id)
    matchs = Match.objects.all().filter(tournoi_id = tournoi.pk)

    nbr_matchs = len(matchs)

    return render(request, 'tournoi.html', {'tournoi': tournoi,'matchs': matchs, 'nbr_matchs': nbr_matchs})


def match_page(request, match_id):
    match = Match.objects.get(pk = match_id)
    tournoi = Tournoi.objects.get(pk = match.tournoi_id)
    message = ''
    messageResultat = ''
    currentTime = timezone.now()

    if currentTime > match.heure_lancement:
        timePassed = True
    else:
        timePassed = False
    
    if request.user.is_authenticated:
        currentBet = Pari.objects.filter(user = request.user, match = match).first()
        if currentBet:
            message = "Vous avez déjà parié sur une loutre sur ce match"

            if match.vainqueur == currentBet.loutre_misee:
                messageResultat = "vous avez gagné 10 points"
            else:
                messageResultat = "Vous avez perdu"

    return render(request, 'match.html', {'match': match, 'message':message, 'tournoi': tournoi, 'timePassed':timePassed, 'resultat':messageResultat})


def register_bet_page(request, tournoi_id, match_id, loutre_id):
    currentMatch = Match.objects.get(pk = match_id)
    tournoi = Tournoi.objects.get(pk = tournoi_id)
    loutremisee = Loutre.objects.get(pk = loutre_id)
    currentTime = timezone.now()

    if currentTime > currentMatch.heure_lancement:
        timePassed = True
    else:
        timePassed = False
    
    if request.user.is_authenticated:
        currentBet = Pari.objects.filter(user = request.user, match = currentMatch).first()
        if currentBet:
            message = "Vous avez déjà parié sur une loutre sur ce match"

            if currentMatch.vainqueur == currentBet.loutre_misee:
                messageResultat = "vous avez gagné 10 points"
            else:
                messageResultat = "Vous avez perdu"
        
        else:
            if timePassed:
                bet = Pari()

                bet.user = request.user
                bet.match = currentMatch
                bet.loutre_misee = loutremisee

                bet.save()
                message = "Pari enregistré"


                if currentMatch.vainqueur == bet.loutre_misee:
                    messageResultat = "Vous avez gagné"

                    request.user.recompense += 10
                    request.user.save()

                else:
                    messageResultat = "Vous avez perdu"
            
            else:
                message = "Vous ne pouvez pas parier sur un match déjà passé"
    
    else:
        message = "Il faut être connecté pour parier"

    return render(request, 'match.html', {'match': currentMatch, 'message':message, 'tournoi': tournoi, 'timePassed':timePassed, 'resultat':messageResultat})