from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.word


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    won = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.word.word}"


class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess = models.CharField(max_length=5)
    guess_number = models.IntegerField()

    def __str__(self):
        return f"{self.game.user.username} - {self.guess}"