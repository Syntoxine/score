from django.contrib import admin

from .models import Player, Score, ScoreEntry

admin.site.register([Player, Score, ScoreEntry])