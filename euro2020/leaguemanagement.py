from common.models import User
from euro2020.models import Team, League, Player, Bids, GamePhase
import random


def setup_bids(league, maxbet):
    currentleague = League.objects.get(pk=league)
    userprefix = currentleague.leaguename + "_"
    playerbidpercentage = 0.8
    teams = Team.objects.filter(name__istartswith=userprefix)
    players = Player.objects.select_related('country').filter(country__openforbid=True)
    print("setup bids is going to make bids for " + str(len(players)) + " players.")
    bidcount = 0
    for team in teams:
        y = random.random()
        team.bidbudget = y * 2000
        team.maxbidgke = y * 3
        team.maxbiddef = y * 8
        team.maxbidmid = y * 8
        team.maxbidatt = y * 5
        team.save()
        for player in players:
            x = random.random()
            if x < playerbidpercentage:
                y = pow(random.random(), 20)
                bid = y * maxbet
                if bid > 1:
                    Bids.objects.create(player=player, playerbid=bid, team=team, gamephase=currentleague.gamephase)
                    bidcount += 1
    print(currentleague.leaguename + ": There have been " + str(bidcount) + " created for this league")
    return


def setup_teams(league):
    # SETUP INITIAL ENVIRONMENT
    # PREREQUISITES: DATABASE, CREATESUPERUSER AND MIGRATE ARE FINISHED. LOADED FIXTURES 01 till 06
    # loaddata 01_country.json 02_location.json 03_gamephase.json 04_leagues.json 05_player.json 06_match.json
    # Script must be run in python console and sets up users, teams, leagues and leaguetables
    currentleague = League.objects.get(pk=league)
    maxteams = currentleague.maxparticipants
    userprefix = currentleague.leaguename + "_"
    usersuffix = '@pokemail.net'
    passwordvalue = "Qwerty12!"

    for i in range(0, maxteams):
        username = userprefix + str(i) + usersuffix
        user = User.objects.create_user(email=username, password=passwordvalue, first_name=username)
        Team.objects.create(owner=user, name=userprefix + "_Team_" + str(i), betcoins=2000, league=currentleague, paid=True)
    currentleague.leaguebalance = 0
    currentleague.save()
    return


def delete_league(league):
    usersuffix = '@pokemail.net'
    # Delete the data from this league. We start with bids
    currentleague=League.objects.get(pk=league)
    userprefix = currentleague.leaguename + "_"
    try:
        bids = Bids.objects.filter(team__name__istartswith=userprefix).delete
        teams = Team.objects.filter(name__istartswith=userprefix).delete
        users = User.objects.filter(email__istartswith=userprefix).delete()
        currentleague.delete()
    except:
        print("something went wrong in deleting the bids, teams, users or league")
    print('end deleting bids')
    return


def nextphase(currentgamephase):
    currentphasenumber = int(str(currentgamephase)[:2])
    phases = GamePhase.objects.all()
    for x in range(currentphasenumber + 1, 100):
        if phases.filter(gamephase__startswith=(str(x) + " ")).exists():
            nextphase = GamePhase.objects.get(gamephase__startswith=(str(x) + " "))
            break
        else:
            nextphase = "The next gamephase did not exist"
    return nextphase


def previousphase(currentgamephase):
    currentphasenumber = int(str(currentgamephase)[:2])
    phases = GamePhase.objects.all()
    for x in range(currentphasenumber - 1, 9, -1):
        if phases.filter(gamephase__startswith=x).exists():
            previousgamephase = GamePhase.objects.get(gamephase__startswith=x)
            previousphase = previousgamephase
            break
        else:
            previousphase = "The previous gamephase did not exist"
    return previousphase
