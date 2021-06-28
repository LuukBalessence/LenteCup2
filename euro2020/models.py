from datetime import datetime, timezone, timedelta

import pytz
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from common.models import User
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    class Country(models.TextChoices):
        NL = "NL", _("Netherlands")
        DE = "DE", _("Germany")
        AZ = "AZ", _("Azerbeijan")
        IR = "IR", _("Ireland")
        ES = "ES", _("Spain")
        RO = "RO", _("Roumania")
        IT = "IT", _("Italy")
        DK = "DK", _("Denmark")
        RU = "RU", _("Russia")
        SC = "SC", _("Scotland")
        UK = "UK", _("England")
        HU = "HU", _("Hungary")

    name = models.CharField(verbose_name=_("Name"), max_length=40, primary_key=True)
    city = models.CharField(verbose_name=_("City"), max_length=40)
    country = models.CharField(
        verbose_name=_("Country"), max_length=2, choices=Country.choices
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return f"{self.name} in {self.city}"


class Country(models.Model):
    class Group(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
        E = "E", "E"
        F = "F", "F"

    name = models.CharField(verbose_name=_("Name"), max_length=30, primary_key=True)
    shortname = models.CharField(verbose_name=_("Ctry"), max_length=3, default="NUL")
    nlname = models.CharField(verbose_name=_("NL naam"), max_length=30, default="")
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Order"), validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    group = models.CharField(
        verbose_name=_("Group"), max_length=1, choices=Group.choices
    )
    openforbid = models.BooleanField(default=False)
    eliminated = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ("group", "order")
        UniqueConstraint(fields=["group", "order"], name="unique_group_order")

    def __str__(self):
        return self.name


class GamePhase(models.Model):
    gamephase = models.CharField(verbose_name=_("Game Phase"), max_length=40, )
    allowbidding = models.BooleanField(default=False)
    allowauction = models.BooleanField(default=False)
    allowlineup = models.BooleanField(default=False)
    allowfiring = models.BooleanField(default=False)
    kophase = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.gamephase}"


class League(models.Model):
    leaguename = models.CharField(verbose_name=_("League Name"), max_length=30, unique=True)
    maxparticipants = models.PositiveSmallIntegerField(verbose_name=_("Max Teams"))
    is_private = models.BooleanField(verbose_name=_("Private League"), default=False)
    gamephase = models.ForeignKey(GamePhase, on_delete=models.CASCADE, related_name="leaguephase")
    leaguebalance = models.PositiveIntegerField(verbose_name=_("League Balance"), validators=[MinValueValidator(0), MaxValueValidator(50000)], default=48000)
    leaguefee = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)
    secretnumber = models.PositiveIntegerField(verbose_name=_("Secret key"), validators=[MinValueValidator(10000), MaxValueValidator(99999)], default=10000)
    draw = models.BooleanField(verbose_name=_("Loting plaatsgevonden"), default=False)
    premiebasis = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.leaguename}"


class Team(models.Model):
    class TeamGroup(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
        E = "E", "E"
        F = "F", "F"

    name = models.CharField(max_length=40)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team')
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="team", null=True, blank=True)
    betcoins = models.PositiveSmallIntegerField(default=0,
                                                validators=([MinValueValidator(0), MaxValueValidator(2000)])
                                                )
    bidbudget = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(2000)])
                                                 )
    maxbidgke = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(3)])
                                                 )
    maxbiddef = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(8)])
                                                 )
    maxbidmid = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(8)])
                                                 )
    maxbidatt = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(5)])
                                                 )
    group = models.CharField(verbose_name=_("Group"), max_length=4, choices=TeamGroup.choices, null=True, blank=True)
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Order"), validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    paid = models.BooleanField(default=False)
    eliminated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "G", _("Goalkeeper")
        DEFENDER = "D", _("Defender")
        MIDFIELDER = "M", _("Midfielder")
        ATTACKER = "A", _("Attacker")

    first_name = models.CharField(verbose_name=_("First name"), max_length=40)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=60)
    position = models.CharField(
        max_length=1, choices=Position.choices
        # verbose_name=_("Position")
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Number"),
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="players"
    )

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        unique_together = (("first_name", "last_name"),)
        ordering = ("country", "position", "number")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Match(models.Model):
    class Stage(models.TextChoices):
        G1 = "G1", _("GroepsRonde 1")
        G2 = "G2", _("GroepsRonde 2")
        G3 = "G3", _("GroepsRonde 3")
        Q6 = "Q6", _("Achtste Finales")
        Q8 = "Q8", _("Kwart Finales")
        Q4 = "Q4", _("Halve Finales")
        Q2 = "Q2", _("Grande Finale")

    stage = models.CharField(
        verbose_name=_("Stage"), max_length=2, choices=Stage.choices
    )
    home = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="home_matches"
    )
    away = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="away_matches"
    )
    players = models.ManyToManyField(to=Player, related_name="matches")
    start = models.DateTimeField(verbose_name=_("Start"))
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name="matches")
    has_started = models.BooleanField(verbose_name=_("Started"), default=False)
    has_ended = models.BooleanField(verbose_name=_("Ended"), default=False)
    verlenging = models.BooleanField(default=False)
    shootout = models.BooleanField(default=False)
    homewonshootout = models.BooleanField(default=False)
    readurl = models.URLField(max_length=300, blank=True)

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")
        ordering = ["start", "id"]

    def __str__(self):
        return f"{self.home} - {self.away}"

    @property
    def is_group_stage(self) -> bool:
        return self.stage in [Match.Stage.G1, Match.Stage.G2, Match.Stage.G3]


class VirtualMatch(models.Model):
    class Stage(models.TextChoices):
        G1 = "G1", _("GroepsRonde 1")
        G2 = "G2", _("GroepsRonde 2")
        G3 = "G3", _("GroepsRonde 3")
        Q6 = "Q6", _("Achtste Finales")
        Q8 = "Q8", _("Kwart Finales")
        Q4 = "Q4", _("Halve Finales")
        Q2 = "Q2", _("Grande Finale")

    stage = models.CharField(
        verbose_name=_("Stage"), max_length=2, choices=Stage.choices
    )
    home = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="hometeam_matches"
    )
    away = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="awayteam_matches"
    )
    start = models.DateTimeField(verbose_name=_("Gestart"))
    end = models.DateTimeField(verbose_name=_("Afgelopen"))
    has_started = models.BooleanField(verbose_name=_("Gestart"), default=False)
    has_ended = models.BooleanField(verbose_name=_("Afgelopen"), default=False)
    verlenging = models.BooleanField(default=False)
    shootout = models.BooleanField(default=False)
    homewonshootout = models.BooleanField(default=False)
    homescore = models.PositiveSmallIntegerField(null=True, blank=True)
    awayscore = models.PositiveSmallIntegerField(null=True, blank=True)
    decimalhomescore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    decimalawayscore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    minusdecimalhomescore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    minusdecimalawayscore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    decimalhomegoalscore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    decimalawaygoalscore = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)

    class Meta:
        verbose_name = _("Virtuele Wedstrijd")
        verbose_name_plural = _("Wedstrijden")
        ordering = ["start", "id"]

    def __str__(self):
        return f"{self.home} - {self.away}"


class Goal(models.Model):
    class Type(models.TextChoices):
        GOAL = "GO", _("Goal")
        PENALTY = "PE", _("Penalty")
        OWN_GOAL = "OG", _("OwnGoal")

    class Phase(models.TextChoices):
        REGULAR = "1R", _("Regular Time")
        EXTRA = "2E", _("Extra Time")
        SHOOTOUT = "3P", _("Penalty Shoot out")

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="goals")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="goals")

    type = models.CharField(
        verbose_name=_("Type of Goal"),
        max_length=2,
        choices=Type.choices,
        default=Type.GOAL,
    )
    minute = models.PositiveSmallIntegerField(
        verbose_name=_("Minute"),
        validators=([MinValueValidator(0), MaxValueValidator(150)]),
    )
    phase = models.CharField(
        verbose_name=_("Phase"),
        max_length=2,
        choices=Phase.choices,
        default=Phase.REGULAR,
    )

    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")
        ordering = ["phase", "minute"]

    def __str__(self):
        return f"{self.player} {self.get_type_display()} {self.minute}"

    def clean(self):
        super().clean()
        # check: in group phase there is no penalty shootout
        if self.phase == Goal.Phase.SHOOTOUT and self.match.is_group_stage:
            raise ValidationError(
                {"phase": _("Group stages don't have a Penalty Shootout phase.")}
            )
        # check if match has started, otherwise goals cannot be added
        now = datetime.now(timezone.utc)
        matchstarts = self.match.start.astimezone(pytz.timezone("UTC"))
        mstarts = matchstarts - timedelta(hours=2)

        if (self.match.has_started) or (now > mstarts):
            print("match started")
        else:
            raise ValidationError(
                {"minute": _("Goals can not be scored when match has not started yet")}
            )


class Bids(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="bids", blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="bids", blank=True)
    playerbid = models.PositiveSmallIntegerField(default=0,
                                                 validators=([MinValueValidator(0), MaxValueValidator(2000)]),
                                                 blank=True)
    gamephase = models.ForeignKey(GamePhase, null=True, on_delete=models.CASCADE)
    assigned = models.BooleanField(null=True)
    bidcomment = models.CharField(verbose_name=_("Bid Comment"), max_length=200, default="Bid Created", null=True)
    previousteam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="bidsprevious", null=True, default=None)
    ontslaan = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")
        ordering = ["team"]

    def __str__(self):
        return f"{self.team} {self.player} {self.playerbid}"


class Boekhouding(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="boekhouding", blank=True)
    boekingsopmerking = models.CharField(verbose_name=_("boekingsopmerking"), max_length=200)
    aantalbetcoins = models.IntegerField(validators=([MinValueValidator(-1), MaxValueValidator(48000)]))


class BoekhoudingLeague(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="boekhoudingleague", blank=True)
    boekingsopmerking = models.CharField(verbose_name=_("boekingsopmerking"), max_length=200)
    aantalbetcoins = models.IntegerField(validators=([MinValueValidator(-48000), MaxValueValidator(48000)]))


class Opstelling(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="opstelling")
    phase = models.ForeignKey(GamePhase, on_delete=models.CASCADE, related_name="opstelling")
    opgesteldespeler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="opstelling")
    nulscore = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    minscore = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    plusscore = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    goalscore = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    verlenging = models.BooleanField(default=False)


class OpstellingLog(models.Model):
    tijdopgesteld = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="opstellinglog")
    phase = models.ForeignKey(GamePhase, on_delete=models.CASCADE, related_name="opstellinglog")
    opgesteldespeler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="opstellinglog")


class Tactiek(models.Model):
    class TactiekKeuze(models.TextChoices):
        G1 = "Normaal", _("Normaal")
        G2 = "Aanvallend", _("Aanvallend")
    tactiek = models.CharField(
        max_length=20, choices=TactiekKeuze.choices
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tactiek")
    phase = models.ForeignKey(GamePhase, on_delete=models.CASCADE, related_name="tactiek")
