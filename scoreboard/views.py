from django.shortcuts import render

from .models import Player, Score, ScoreEntry


def index(request):
    context = {
        "scores": Score.objects.all(),
        "players": Player.objects.all(),
    }
    return render(request, "scoreboard/index.html", context=context)


def score(request, score_name):
    score = Score.objects.get(name=score_name)
    context = {
        "score": score,
        "entries": ScoreEntry.objects.filter(score__id=score.id).order_by("-value"),
        "view_type": "score",
    }
    return render(request, "scoreboard/detail.html", context=context)


def player(request, player_name):
    player = Player.objects.get(name=player_name)
    entries = ScoreEntry.objects.filter(player__id=player.id).order_by("-value")
    context = {
        "player": player,
        "entries": entries,
        "view_type": "player",
    }
    return render(request, "scoreboard/detail.html", context=context)
