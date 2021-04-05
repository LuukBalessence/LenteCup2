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
        return f"{self.score}"


class Speler(models.Model):
    rank = models.PositiveSmallIntegerField()
    first_name = models.CharField(verbose_name=("First name"), max_length=40)
    last_name = models.CharField(verbose_name=("Last name"), max_length=60)
    land = models.CharField(max_length=40)
    position = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = ("Speler")
        verbose_name_plural = ("Spelers")
        unique_together = (("first_name", "last_name"),)
        ordering = ("rank", "first_name", "last_name")

    def __str__(self):
        return f"{self.rank} {self.first_name} {self.last_name}"


class GekozenSpelers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gekozen")
    speler = models.ForeignKey(Speler, on_delete=models.CASCADE, related_name="gekozen")
    eindplaats = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (("user", "speler"),)
        ordering = ("user", "speler")

    def __str__(self):
        return f"{self.user} {self.speler}"