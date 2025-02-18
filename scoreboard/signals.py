from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import transaction

from .models import ScoreEntry


@receiver(post_save, sender=ScoreEntry)
@receiver(post_delete, sender=ScoreEntry)
def update_ranks(sender, instance, **kwargs):
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