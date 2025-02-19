import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

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

def modify_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            player = get_object_or_404(Player, id=data["player_id"])
            score = get_object_or_404(Score, id=data["score_id"])
            value_change = int(data["value"])

            # Retrieve or create the ScoreEntry
            entry, created = ScoreEntry.objects.get_or_create(player=player, score=score, defaults={"value": 0})
            entry.value += value_change
            entry.save()

            updated_entries = list(
                ScoreEntry.objects.filter(score=score).order_by("-value").values("player__id", "player__name", "value", "rank")
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"score_{score.id}",
                {
                    "type": "update_scoreboard",
                    "data": {"entries": updated_entries},
                },
            )

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
