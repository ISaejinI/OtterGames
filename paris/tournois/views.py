from django.shortcuts import render, get_object_or_404
from .models import Match

def match_page(request, match_id):
    match = Match.objects.get(pk = match_id)




    return render(request, 'match.html', {'match': match})