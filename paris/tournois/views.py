from django.shortcuts import render, get_object_or_404, redirect
from .models import Match, Tournoi, Loutre, Pari

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
    loutre1 = Loutre.objects.get(pk = match.loutre1_id)
    loutre2 = Loutre.objects.get(pk = match.loutre2_id)

    if request.method == 'POST':
        loutre_id = request.POST.get('loutre_gagante')
        print(loutre_id)
        loutre_misee = get_object_or_404(Loutre, id=loutre_id)

        # Crée ou update le pari pour ce user & match
        pari, created = Pari.objects.get_or_create(
            user=request.user,
            match=match,
            defaults={'loutre_misee': loutre_misee}
        )

        if not created:
            pari.loutre_misee = loutre_misee
            print(loutre_id)
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


