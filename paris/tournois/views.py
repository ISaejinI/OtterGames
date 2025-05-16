from django.shortcuts import render, get_object_or_404
from .models import Match, Tournoi, Loutre

def match_page(request, match_id):
    match = Match.objects.get(pk = match_id)
    tournoi = Tournoi.objects.get(pk = match.tournoi_id)
    loutre1 = Loutre.objects.get(pk = match.loutre1_id)
    loutre2 = Loutre.objects.get(pk = match.loutre2_id)

    return render(request, 'match.html', {'match': match, 'tournoi': tournoi, 'loutre1': loutre1, 'loutre2': loutre2})