from django.db import models
from common.models import User

class GolfProfiel(models.Model):
    naam = models.CharField(max_length=40)
    eigenaar = models.OneToOneField(User, on_delete=models.CASCADE, related_name='golfprofiel')
    ehcp = models.DecimalField(max_digits=3, decimal_places=1)
    lohcp = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    verraders = models.BooleanField(default=False)
    ziener = models.BooleanField(default=False)
    buggy = models.BooleanField(default=False)
    huurset = models.BooleanField(default=False)
    preluukopen = models.BooleanField(default=False)
    opmerking = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.naam}"


class BaanProfiel(models.Model):
    naam = models.CharField(max_length=60)
    plaats = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.naam}"


class TeeKleur(models.Model):
    kleur = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.kleur}"


class GolfBaanProfiel(models.Model):
    naam = models.CharField(max_length=60)
    aantalholes = models.PositiveIntegerField(default=9)
    sr = models.DecimalField(max_digits=3, decimal_places=0, blank=True)
    cr = models.DecimalField(max_digits=3, decimal_places=1, blank=True)
    par = models.DecimalField(max_digits=3, decimal_places=1, blank=True)
    baan = models.ForeignKey(BaanProfiel, on_delete=models.CASCADE, related_name="golfbaan")
    teekleur = models.ForeignKey(TeeKleur, on_delete=models.CASCADE, related_name="golfbaan")

    def __str__(self):
        return f"{self.naam} {self.teekleur}"


class Holes(models.Model):
    hole_nr = models.PositiveIntegerField()
    par = models.PositiveIntegerField()
    strokeindex = models.PositiveIntegerField()
    afstand = models.PositiveIntegerField(blank=True)
    golfbaan = models.ForeignKey(GolfBaanProfiel, on_delete=models.CASCADE, related_name="holes")

    def __str__(self):
        return f"{self.golfbaan} {self.hole_nr}"
