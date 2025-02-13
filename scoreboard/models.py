from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=256)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.score} points)"
