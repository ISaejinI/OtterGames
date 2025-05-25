from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Tournoi, Loutre, Pari
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
    currentTime = datetime.datetime.now()

    return render(request, 'match.html', {'match': match, 'message':'', 'tournoi': tournoi, 'currentTime':currentTime})


def register_bet_page(request, tournoi_id, match_id, loutre_id):
    currentMatch = Match.objects.get(pk = match_id)
    tournoi = Tournoi.objects.get(pk = tournoi_id)
    loutremisee = Loutre.objects.get(pk = loutre_id)
    currentTime = datetime.datetime.now()

    currentBet = Pari.objects.get(user = request.user, match = currentMatch)
    
    if request.user.is_authenticated:
        if currentBet:
            message = "Vous avez déjà parié sur une loutre sur ce match"
        
        else:
            bet = Pari()

            bet.user = request.user
            bet.match = currentMatch
            bet.loutre_misee = loutremisee

            bet.save()
            message = "Pari enregistré"
    
    else:
        message = "Il faut être connecté pour parier"

    if currentMatch.vainqueur == bet.loutre_misee:
        message = "vous avez gagné"
    else:
        message = "Vous avez perdu"
    

    return render(request, 'match.html', {'match': currentMatch, 'message':message, 'tournoi': tournoi, 'currentTime':currentTime})