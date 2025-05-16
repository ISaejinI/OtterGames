from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Tournoi, Loutre, Pari

def match_page(request, match_id):
    match = Match.objects.get(pk = match_id)
    tournoi = Tournoi.objects.get(pk = match.tournoi_id)
    loutre1 = Loutre.objects.get(pk = match.loutre1_id)
    loutre2 = Loutre.objects.get(pk = match.loutre2_id)

    if request.method == 'POST':
        loutre_id = request.POST.get('loutre_gagante')
        loutre_misee = get_object_or_404(Loutre, id=loutre_id)

        # Crée ou update le pari pour ce user & match
        pari, created = Pari.objects.get_or_create(
            user=request.user,
            match=match,
            defaults={'loutre_misee': loutre_misee}
        )

        if not created:
            pari.loutre_misee = loutre_misee
            pari.save()

        # Directement vérifier si le pari est bon
        if match.vainqueur:
            if pari.loutre_misee == match.vainqueur:
                pari.resultat = True
                request.user.recompense += 1
                request.user.save()
            else:
                pari.resultat = False

            pari.save()

        return redirect('detail_match', match_id=match.id)

    return render(request, 'match.html', {'match': match, 'tournoi': tournoi, 'loutre1': loutre1, 'loutre2': loutre2})