from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from common.models import User


class Week(models.Model):
    week = models.CharField(max_length=21)
    weeknummer = models.PositiveSmallIntegerField(validators=([MinValueValidator(1), MaxValueValidator(53)]), null=True)
    maxpoints = models.PositiveSmallIntegerField(default=4)
    openforscoring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.week}"


class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores", blank=True)
    score = models.PositiveSmallIntegerField(validators=([MinValueValidator(0), MaxValueValidator(40)]))
    qualifying = models.BooleanField(null=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="scores", blank=True)
    baan = models.CharField(max_length=40, blank=True)
    lus = models.CharField(max_length=40, blank=True    )
    finalscore = models.DecimalField(decimal_places=2, max_digits=5, default=0, blank=True)

    def __str__(self):
        return f"{{self.score}}"