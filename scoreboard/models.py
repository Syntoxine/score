from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Score(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ScoreEntry(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "score"], name="unique_player_score"
            )
        ]

    def __str__(self):
        return f"{self.player} [{self.score}] ({self.value} points)"
