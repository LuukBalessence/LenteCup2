from django.test import TestCase

from wk2022.models import Country, Player, Goal, Match, Location


class EmptyDatabaseTests(TestCase):
    def test_there_are_no_objects(self):
        self.assertTrue(Country.objects.all().count() == 0)
        self.assertTrue(Player.objects.all().count() == 0)
        self.assertTrue(Goal.objects.all().count() == 0)
        self.assertTrue(Match.objects.all().count() == 0)

    def test_add_location(self):
        location = Location(city="Alkmaar", country="NL", name="AFAS Stadion")
        location.save()
        self.assertTrue(Location.objects.filter(name__startswith="AFAS").exists())

    def test_add_country(self):
        country = Country(group=Country.Group.A.value, name="Nederland", order=1)
        country.save()
        self.assertTrue(Country.objects.filter(name="Nederland").exists())

    def test_add_player(self):
        country = Country(group=Country.Group.A.value, name="Nederland", order=1)
        country.save()
        player = Player(
            country=country,
            first_name="Daniel",
            last_name="van der Meulen",
            number=11,
            position=Player.Position.ATTACKER.value,
        )
        player.save()
        self.assertFalse(
            Player.objects.filter(first_name="Luuk", last_name="Smeets").exists()
        )
        self.assertTrue(
            Player.objects.filter(
                first_name="Daniel", last_name="van der Meulen"
            ).exists()
        )

    def test_add_match(self):
        location = Location(city="Alkmaar", country="NL", name="AFAS Stadion")
        location.save()
        nl = Country(group=Country.Group.A.value, name="Nederland", order=1)
        nl.save()
        de = Country(group=Country.Group.A.value, name="Duitsland", order=2)
        de.save()
        match = Match(location=location, start="2020-06-21 19:45", home=nl, away=de)
        match.save()
        self.assertTrue(
            Match.objects.filter(home="Nederland", away="Duitsland").exists()
        )

    # TODO: voor Luuk
    def test_add_goal(self):
        location = Location(city="Alkmaar", country="NL", name="AFAS Stadion")
        location.save()
        wl = Country(group=Country.Group.B.value, name="Wales", order=1)
        wl.save()
        sw = Country(group=Country.Group.B.value, name="Switzerland", order=2)
        sw.save()
        match = Match(location=location, start="2020-06-21 19:45", home=nl, away=de)
        match.save()
        welshplayer = Player(
            country = country,
            first_name = "Gareth",
            last_name = "Bale",
            number = 11,
            position = Player.Position.DEFENDER.value,
        )
        welshplayer.save()
        goal = Goal(
            player = welshplayer,
            type = Goal.Type.GOAL.value,
            minute = 44,
            phase = Goal.Phase.REGULAR.value
        )
        goal.save()
        self.assertTrue(
            Goal.objects.filter(player=welshplayer, minute=44).exists()
            )

class FilledDatabaseTest(TestCase):
    fixtures = ["location", "country", "player"]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_netherlands_in_group_c(self):
        self.assertTrue(Country.objects.filter(name="Netherlands", group="C").exists())

    def test_netherlands_has_more_than_11_players(self):
        self.assertGreater(Player.objects.filter(country="Netherlands").count(), 11)

    # TODO: voor Luuk, verzin een aantal tests, hoeven niet zinvol te zijn maar zodat je een beetje
    # leert hoe testen werkt in Django, bijvoorbeeld:
    def test_there_are_24_countries(self):
        self.assertTrue(Country.objects.all().count(), 24)

    def test_there_are_6_groups(self):
        self.assertTrue(Country.Group.objects.all().count(), 6)

    def test_there_are_4_countries_in_each_group(self):
        for group in Country.Group:
            self.assertTrue(Country.objects.filter(group=group).count(), 4)

    def test_there_are_minimal_15_players_per_country(self):
        for country in Country:
            self.assertGreater(Player.objects.filter(country=country).count(), 15)

    def test_total__group_matches_equals_24(self):
        self.assertTrue(Match.objects.all().count(), 24)


