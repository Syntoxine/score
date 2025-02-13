from django.shortcuts import render

from .models import Player


# Create your views here.
def index(request):
    return render(request, "scoreboard/index.html", {'players': Player.objects.all()})
