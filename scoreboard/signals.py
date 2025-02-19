from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import transaction

from .models import ScoreEntry, Score, Player


@receiver(post_save, sender=Score)
def create_score_entries(sender, instance, created, **kwargs):
    """Creates a ScoreEntry for every Player when a new Score is created."""
    if created:
        players = Player.objects.all()
        score_entries = [
            ScoreEntry(player=player, score=instance)
            for player in players
        ]
        ScoreEntry.objects.bulk_create(score_entries)

@receiver(post_save, sender=Player)
def create_missing_score_entries(sender, instance, created, **kwargs):
    """Creates a ScoreEntry for new Players in all existing Scores."""
    if created:
        scores = Score.objects.all()
        score_entries = [
            ScoreEntry(player=instance, score=score, value=0, rank=1)
            for score in scores
        ]
        ScoreEntry.objects.bulk_create(score_entries)


@receiver(post_save, sender=ScoreEntry)
@receiver(post_delete, sender=ScoreEntry)
def update_ranks(sender, instance, **kwargs):
    """Updates the ranks of all ScoreEntries in the same Score when a ScoreEntry is modified."""
    score = instance.score
    entries = ScoreEntry.objects.filter(score=score)

    updates = []
    for entry in entries:
        rank = entries.filter(value__gt=entry.value).count() + 1
        if entry.rank != rank:
            entry.rank = rank
            updates.append(entry)

    if updates:
        with transaction.atomic():
            ScoreEntry.objects.bulk_update(updates, ['rank'])