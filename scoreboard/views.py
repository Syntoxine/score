from django.shortcuts import render

from .models import Player, Score, ScoreEntry


def index(request):
    context = {"scores": Score.objects.all(), "players": Player.objects.all()}
    return render(request, "scoreboard/index.html", context=context)


def score(request, score_name):
    score = Score.objects.get(name=score_name)
    context = {
        "score": score,
        "entries": ScoreEntry.objects.filter(score__id=score.id).order_by("-value"),
    }
    return render(request, "scoreboard/score.html", context=context)


def player(request, player_name):
    player = Player.objects.get(name=player_name)
    entries = ScoreEntry.objects.filter(player__id=player.id).order_by("-value")
    ranked_entries = [ScoreEntry.objects.filter(score=entry.score, value__gt=entry.value).count() + 1 for entry in entries]
    context = {
        "player": player,
        "entries": zip(entries, ranked_entries),
    }
    return render(request, "scoreboard/player.html", context=context)
