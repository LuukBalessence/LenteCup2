import random

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect

from LenteCup2.models import GameSettings
from common.models import AppAuthorisation, Apps
from euro2020 import models
from euro2020.models import Bids, Player, League, GamePhase, Boekhouding, BoekhoudingLeague
from .bid_functions import createbidlist, validbid, assignfinalbid, savebid, remove_sameplayer_bids, \
    saveteaminfo
from .forms import ChangeFirstNameForm, ChangeTeamNameForm, AddGoalForm, BidsForm, CreateLeagueForm, PickLeagueForm
from .leaguemanagement import setup_teams, setup_bids, delete_league, previousphase, nextphase
from .scoring_functions import (
    match_results,
    group_standings,
    equalityofpoints,
    getmatchlist,
    getgoallist,
    recalculateposition,
)
from .models import Match, Goal, Country, Team
from django.forms import formset_factory


def index(request):
    if request.user.is_authenticated:
        return redirect(to="euro2020")

    countries = get_list_or_404(klass=models.Country)
    groups = models.Country.Group.names
    players = models.Player.objects.select_related("country")
    locations = get_list_or_404(klass=models.Location)
    match = get_list_or_404(klass=models.Match)

    return render(
        request,
        template_name="euro2020/index.html",
        context={
            "countries": countries,
            "groups": groups,
            "players": players,
            "locations": locations,
            "match": match,
        },
    )


def standenbeheer(request):
    matches = Match.objects.all().prefetch_related("home", "away")

    return render(
        request,
        template_name="euro2020/standenbeheer.html",
        context={"matches": matches, },
    )


def add_goal(request, pk: int):
    # voorbeeld hoe je een doelpunt toevoegt, parameter pk is de id van een match
    # we maken eerst een nieuwe instance van GoalScoring aan waar we de match alvast invullen
    # dan maak je het formulier waar de goal kan worden ingevuld

    match = get_object_or_404(Match, pk=pk)
    instance = Goal(
        match=match
    )  # goal wordt gescoord in een match, dus match is een gegeven

    if request.method == "POST":
        form = AddGoalForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(to="standenbeheer")
        else:
            print(form.errors)
    else:
        form = AddGoalForm(instance=instance)

    return render(
        request=request, template_name="euro2020/add_goal.html", context={"form": form}
    )


def euro2020(request):
    hoofdmelding1 = GameSettings.objects.get(gamesettings='hoofdmelding1').gamesettingsvalue
    hoofdmelding2 = GameSettings.objects.get(gamesettings='hoofdmelding2').gamesettingsvalue
    hoofdmelding3 = GameSettings.objects.get(gamesettings='hoofdmelding3').gamesettingsvalue
    hoofdmelding4 = GameSettings.objects.get(gamesettings='hoofdmelding4').gamesettingsvalue
    return render(request, template_name="euro2020/euro2020.html", context={"hoofdmelding1": hoofdmelding1,
                                                                            "hoofdmelding2": hoofdmelding2,
                                                                            "hoofdmelding3": hoofdmelding3,
                                                                            "hoofdmelding4": hoofdmelding4})


def changefirstname(request):
    if request.method == 'POST':
        form = ChangeFirstNameForm(request.POST)
        if form.is_valid():
            namedata = form.cleaned_data
            currentuser = request.user
            currentuser.first_name = namedata.get('firstname')
            currentuser.save()
            return redirect(to="myaccount")
        else:
            return render(request, "euro2020/changefirstname.html", {'form': ChangeFirstNameForm})
    #
    else:
        return render(request, template_name="euro2020/changefirstname.html")


def changeteamname(request):
    error = ""
    app = Apps.objects.get(appname="EURO 2020")
    try:
        currentuser = request.user
        teamcurrentuser = Team.objects.get(owner=currentuser)
    except ObjectDoesNotExist:
        teamcurrentuser = ""

    if request.method == 'POST':
        form = ChangeTeamNameForm(request.POST)
        if form.is_valid():
            namedata = form.cleaned_data
            teamname = namedata.get('teamname')

            # Eerst controleren of de op het formulier ingevoerde teamnaam al niet bestaat
            try:
                # Case insensitive check
                teamtochange = Team.objects.get(name__icontains=teamname)
                if teamtochange:
                    error = "teamexists"
                    return render(request, "euro2020/changeteamname.html", context={"error": error})
            except:
                if teamcurrentuser:
                    # Als de teamnaam nog niet bestaat dient deze te worden geregistreerd bij degene die is aangemeld.
                    # Eerst kijken of de huidige gebruiker al een naam heeft geregistreerd.
                    Team.objects.filter(owner=currentuser).update(name=teamname)
                else:
                    Team.objects.create(name=teamname, owner=currentuser)
                    AppAuthorisation.objects.create(app=app, user=currentuser)
                return redirect(to="myteam")
        else:
            return render(request, "euro2020/changeteamname.html", context={'form': ChangeTeamNameForm, "error": error})

    else:
        return render(request, template_name="euro2020/changeteamname.html")


def myteam(request):
    leaguedraw = False
    bidauction = False
    manager = request.user
    bnumber = GameSettings.objects.get(gamesettings='bnumber').gamesettingsvalue
    bname = GameSettings.objects.get(gamesettings='bname').gamesettingsvalue
    leaguefee = "Onbekend"
    try:
        teamdata = Team.objects.get(owner=manager)
    except:
        teamdata = ""
    try:
        league = teamdata.league
        if league == None:
            league = ""
        else:
            leaguefee = league.leaguefee
            leaguedraw = league.draw


    except:
        league = ""

    try:
        leaguephase = league.gamephase
        if leaguephase.allowbidding or leaguephase.allowauction:
            bidauction = True
    except:
        leaguephase = ""

    betcoinbalance = ""
    try:
        if teamdata.paid:
            betcoinbalance = teamdata.betcoins
    except:
        betcoinbalance = ""

    try:
        team = Team.objects.get(owner=manager)
        return render(request, template_name="euro2020/myteam.html",
                      context={"team": team, "tactics": team, "lineup": team, "league": league,
                               "leaguephase": leaguephase,
                               "betcoinbalance": betcoinbalance, "bidauction": bidauction, "bnumber": bnumber,
                               "bname": bname
                          , "leaguefee": leaguefee, "leaguedraw": leaguedraw})
    except ObjectDoesNotExist:
        return redirect(to="changeteamname")


def myleague(request):
    manager = request.user
    try:
        teamdata = Team.objects.get(owner=manager)
    except:
        teamdata = ""
    try:
        league = League.objects.get(leaguename=teamdata.league)
    except:
        league = ""
    try:
        leaguephase = league.gamephase
        if leaguephase.allowbidding or leaguephase.allowauction:
            bidauction = True
    except:
        leaguephase = ""

    betcoinbalance = ""
    try:
        if teamdata.paid:
            betcoinbalance = teamdata.betcoins
    except:
        betcoinbalance = ""

    return render(request, template_name="euro2020/myleague.html",
                  context={"league": league, "teamdata": teamdata})


def rleuro2020(request):
    return render(request, template_name="euro2020/rleuro2020.html")


def pickleague(request):
    error = ""
    availableleagues = []
    leagues = League.objects.filter(draw=False)
    for league in leagues:
        teams = Team.objects.filter(league=league.pk)
        if len(teams) < 24:
            availableleagues.append(league)
    form = PickLeagueForm()
    if request.method == 'POST':
        form = PickLeagueForm(request.POST)
        if form.is_valid():
            namedata = form.cleaned_data
            leaguename = namedata.get('leaguename')
            if leaguename == "Kies een league":
                error = "Je dient een league te kiezen of terug te gaan naar het hoofdmenu"
                return render(request, template_name="euro2020/pickleague.html",
                              context={"leagues": leagues, "availableleagues": availableleagues, "error": error})
            manager = request.user
            try:
                team = Team.objects.get(owner=manager)
            except:
                error = "You do not have a team name yet. Please go to the My Account menu"
                return render(request, template_name="euro2020/pickleague.html",
                              context={"leagues": leagues, "availableleagues": availableleagues, "error": error})
            team.league = League.objects.get(leaguename=leaguename)
            team.save()
            return redirect(myteam)

    return render(request, template_name="euro2020/pickleague.html",
                  context={"form": form, "leagues": leagues, "availableleagues": availableleagues, "error": error})


def listallbids(request):
    manager = request.user
    try:
        currentteam = Team.objects.get(owner=manager)
    except ObjectDoesNotExist:
        error = "Please create a team first. Go to the Change Team page located in My Account"
        return render(request, 'euro2020/listallbids.html',
                      context={'countries': "", 'bids': "", 'error': error})

    allteambids = Bids.objects.filter(team=currentteam).order_by('playerbid').reverse()
    return render(request, 'euro2020/listallbids.html',
                  context={'countries': Country.objects.all(), 'bids': allteambids, 'error': ""})


def groepstand(request):
    results = match_results(Match.objects.all(), Goal.objects.all())
    standings = group_standings(results, Country.objects.all())
    standings.sort(key=lambda x: (x.country.group, -x.GS, -x.PT, x.DF, -x.DV))
    rankproperty = "PT"
    # standings.sort(key=eufa_sort)
    # We mark the countries who have equal points with equalPT, False means that countries with 0 matches are discarded
    equalcountries = equalityofpoints(standings, rankproperty, False)
    print("First", equalcountries)

    # a) Get the teams in the same group with same results define by POCOMMENT,
    # a) and calculate standings among teams in question
    #
    matches_a_c = getmatchlist(equalcountries)
    goals_a_c = getgoallist(matches_a_c)
    print(goals_a_c)
    results1 = match_results(matches_a_c, goals_a_c)
    standings1 = group_standings(results1, equalcountries)
    standings1.sort(key=lambda x: (x.country.group, -x.GS, -x.PT, x.DF, -x.DV))
    equalcountries1 = equalityofpoints(standings1, rankproperty, True)
    print("First", equalcountries1)
    recalculateposition(standings, equalcountries1)
    standings.sort(key=lambda x: (x.country.group, x.PO))

    # After first calculation of standings, also matches.GS==0 must be displayed. Check. Done

    return render(
        request=request,
        template_name="euro2020/groepstand.html",
        context={"groupdata": standings, "groups": Country.Group.labels}
    )


def leaguestand(request, league):
    currentleague = League.objects.get(pk=league)
    leagueteams = Team.objects.filter(league=league).order_by("order")
    return render(
        request=request,
        template_name="euro2020/leaguestand.html", context={"loting": currentleague.draw, "groups": Team.TeamGroup.labels, "leagueteams": leagueteams})


def bidoverview(request):
    league = ""
    disabled = ""
    error = ""
    manager = request.user
    team = Team.objects.get(owner=manager)
    try:
        currentteam = Team.objects.get(owner=manager)
        # Als de huidige gebruiker een team heeft dienen we te controleren of deze toegewezen is aan een league
        try:
            currentleague = currentteam.league
            currentleaguegamephase = League.objects.get(leaguename=currentleague).gamephase
            if not GamePhase.objects.get(gamephase=currentleaguegamephase).allowbidding:
                error = "Je league is (nog) niet in een fase die biedingen toelaat"
        except:
            error = "Je hebt nog geen league gekozen. Ga in het Hoofdmenu naat  Jouw Team"
            # We dienen te controleren of we in een spelfase zitten waarin we mogen bieden, anders een melding
    except ObjectDoesNotExist:
        error = "Je dient eerst een teamnaam aan te maken onder Jouw teamgegevens"

    try:
        league = team.league
        leaguephase = league.gamephase
        if leaguephase.allowauction:
            disabled = "disabled"
    except:
        pass

    if request.method == 'POST':
        if request.POST.get("bewaarveiling"):
            team.bidbudget = request.POST['maxbetcoin']
            team.maxbidgke = request.POST['gke']
            team.maxbiddef = request.POST['def']
            team.maxbidmid = request.POST['mid']
            team.maxbidatt = request.POST['att']
            team.save()
            error1 = "Je instellingen zijn opgeslagen"
            return render(request, "euro2020/bidoverview.html",
                          context={'countries': Country.objects.all(), 'groups': Country.Group.labels,
                                   "league": league, "disabled": disabled, "team": team, "error": error, "error1": error1})
        else:
            pass

    return render(request, "euro2020/bidoverview.html",
                  context={'countries': Country.objects.all(), 'groups': Country.Group.labels,
                           "league": league, "disabled": disabled, "team": team, "error": error})


def bids(request, country_name):
    # TODO Test Tab function on Iphone
    BidFormSet = formset_factory(BidsForm)
    formset = BidFormSet(initial=[])
    country = Country.objects.get(name=country_name)
    countries = Country.objects.all()
    countrybidopen = country.openforbid

    # Wat is de naam van de huidige manager en heeft hij al een team?
    manager = request.user
    try:
        currentteam = Team.objects.get(owner=manager)
    except ObjectDoesNotExist:
        error = "Please create a team first. Go to the Change Team page located in My Account"
        return render(request, 'euro2020/bids.html',
                      context={'formset': formset, 'error': error})
    # Als de huidige gebruiker een team heeft dienen we te controleren of deze toegewezen is aan een league
    try:
        currentleague = currentteam.league
    except:
        error = "You have not been assigned to a league yet. If the bidding window is open, " \
                "please ask the administrator to do so"
        return render(request, 'euro2020/bids.html',
                      context={'formset': "", 'error': error})
    # We dienen te controleren of we in een spelfase zitten waarin we mogen bieden, anders een melding
    currentleaguegamephase = League.objects.get(leaguename=currentleague).gamephase

    if not GamePhase.objects.get(gamephase=currentleaguegamephase).allowbidding:
        print("The gamephase of this league = ", currentleaguegamephase, ". This phase is not open for bidding")
        error = "Your league is not in a gamephase which is open for bidding"
        return render(request, 'euro2020/bids.html',
                      context={'formset': "", 'error': error})

    # We creeren eerst een biedinglijst voor het team van de ingelogde gebruiker
    # Deze lijst bestaat uit de reeds gedane beidingen aangevuld met lege biedingen voor de spelers
    # waarop nog niet is geboden
    initialbids = createbidlist(currentteam, country_name)

    # Bij versturen formulier controleren we of deze valide is.
    if request.method == 'POST':
        formset = BidFormSet(request.POST, initial=initialbids)
        if formset.is_valid():
            if formset.has_changed():
                i = 0
                for form in formset:
                    if form.has_changed():
                        # Voor elk veranderd formulier in de formset achterhalen we het spelersid en kijken we of
                        # er al een bieidng voor is. Zo niet dan creeren we de bieding. Anders doen we een update.
                        # Een bieding van 0 halen we weg uit de biedingenlijst.
                        currentplayer = Player.objects.get(pk=form.cleaned_data["playerpk"])
                        try:
                            obj = Bids.objects.get(team=currentteam, player=currentplayer, gamephase=currentleaguegamephase)
                            obj.playerbid = form.cleaned_data["bid"]
                            if obj.playerbid == 0 or obj.playerbid == "None":
                                obj.delete()
                            else:
                                obj.save()
                        # We voegen de gamephase toe aan de bieding om
                        except:
                            if form.cleaned_data["bid"] > 0:
                                obj1 = Bids.objects.create(
                                    team=currentteam, player=currentplayer, playerbid=form.cleaned_data["bid"],
                                    gamephase=GamePhase.objects.get(gamephase=currentleaguegamephase),
                                    bidcomment="Bid Created")
                                obj1.save()
                        i += 1
                print(i, " changes made")
            else:
                print("No  fields have changed")
            # data = BidFormSet(request.POST)
            print("ending if changed loop")
            # Als er op de Save bids knop gedrukt wordt krijgt de gebruiker weer hetzlefde land te zien met de
            # gedane aanpassingen
            # Als er op de Save & Go to knop wordt gedrukt, wordt de pagina met biedingen van het
            # nieuw gekozen land geladen
            if request.POST.get("save_and_go"):
                country_name = request.POST['selectcountry']
        else:
            print("The formset is invalid")
        return redirect(bids, country_name=country_name)
    else:
        formset = BidFormSet(initial=initialbids)

    return render(request, 'euro2020/bids.html',
                  context={'formset': formset, 'countries': countries, 'countryname': country_name,
                           'countrybidopen': countrybidopen})


def auction(request, league, gamephase):
    # Aanpak: We selecteren alle biedingen voor een bepaalde league en maken daar een list van (bidstoprocess).
    # We sorteren de lijst en wijzen de hoogste bieding voor een speler toe en wijzen alle andere biedingen af.
    # Uiteindelijke slaan we de lijst op in het Bids model. We halen alleen in het begin gegevens uit de
    #  database om de perfomance zo goed mogelijk te houden. Alleen als een bieding wordt toe- of afgewezen slaan we hem op
    # Op het eind slaan we ook de teamgegevens op (uitgegeven budget etc..)
    # TODO ontslaan spelers. kan tot maar niet tijdens de biedfase.
    # TODO veilingen na 1e veiling.
    # TODO lijst met niet verkochte spelers in ene veiling (komen terug in de volgende veiling
    # TODO toewijzen spelers als mensen geen volledig team hebben?
    # TODO Hoe bepaal je in welk team een speler zit na de groepsfase?
    # TODO Volgens mij mag er niet ontslagen worden tijdens biedingen en veiling van de groepsfase? Check
    # TODO hoeveel geld beschikbaar en hoeveel uitkeren na elke ronde?
    # TODO Check op minimaal 1000 betcoins uitgegeven
    # TODO simuleerfunctie voor ontslaan spelers

    error = ""
    #  Dit is een admin functie.
    currentuser = request.user
    if not currentuser.is_superuser:
        error = "You must be a super user to start the auction"
        return render(request, 'euro2020/assignedbidsperteam.html',
                      context={'bids': "", 'teams': "", 'error': error})
    # We halen de alle team uit deze league op en alle bijbehorende biedingen. We sorteren deze

    currentleague = League.objects.get(pk=league)
    if not currentleague.gamephase.allowauction:
        error = "The current game phase " + str(currentleague.gamephase) + " does not allow an auction to be performed"
        return render(request, 'euro2020/assignedbidsperteam.html',
                      context={'bids': "", 'teams': "", 'error': error})

    allteams = Team.objects.filter(league__leaguename=currentleague.leaguename).values()
    players = list(Player.objects.filter().values())
    currentphase = currentleague.gamephase
    previousgamephase = previousphase(currentphase)
    allbids = Bids.objects.select_related('player').filter(team__in=list(allteams.values_list()),
                                                           gamephase=previousgamephase, assigned=None)
    print("I collected " + str(len(allbids)) + " bids with gamephase " + str(previousgamephase))
    bidstoprocess = list(allbids.values())
    for bid in bidstoprocess:
        bid['assigned'] = None
    teamsinfo = list(allteams.values())
    for team in teamsinfo:
        team['gkecount'] = 0
        team['defcount'] = 0
        team['midcount'] = 0
        team['attcount'] = 0
        team['budgetgkecount'] = 0
        team['budgetdefcount'] = 0
        team['budgetmidcount'] = 0
        team['budgetattcount'] = 0

    # Als dat is gebeurt, halen we de hoogste biedingen uit de alle-biedingen lijst.
    # Zolang er biedingen zijn, wijzen we er 1 toe, wijzen de anderen met biedngen op dezelfde speler af
    # Totdat de biedingen op zijn. Bij ene toe- of afwijzing wordt processed=True gezet
    while bidstoprocess:
        teamstoprocess = []
        highestbids = []
        highestbid = max([x['playerbid'] for x in bidstoprocess])
        for bid in bidstoprocess:
            team = list(filter(lambda x: x['id'] == bid['team_id'], teamsinfo))[0]
            checkbid = validbid(bid, team, players)
            if checkbid[0]:
                if bid['playerbid'] == highestbid:
                    highestbids.append(bid)
                    if not team in teamstoprocess:
                        teamstoprocess.append(team)
            else:
                savebid(bid, False, checkbid[1], team, players)
                bidstoprocess.remove(bid)
        if not len(highestbids) == 0:
            print('CASE II. ' + str(len(highestbids)) + ' bid(s) needs to be assigned with value: ' + str(highestbid))
            finalbid = assignfinalbid(highestbids, teamstoprocess, players)
            bidstoprocess.remove(finalbid[0])
            remove_sameplayer_bids(bidstoprocess, finalbid[0]['player_id'], teamsinfo)
            print("Er zijn nog " + str(len(bidstoprocess)) + " biedingen")

        # Pas teamgegevens aan
        # We verlaten de for loop en starten met de nieuwe hoogste bieding

    saveteaminfo(teamsinfo)
    print("EINDE: Er zijn nog " + str(len(bidstoprocess)) + " biedingen")
    return redirect(leagueoverview)


def assignedbidsperteam(request, league):
    currentleague = League.objects.get(pk=league)
    teams = Team.objects.filter(league=currentleague).values()
    bids = Bids.objects.select_related('player').filter(team__in=list(teams.values_list()), assigned=True).order_by(
        '-playerbid')
    return render(request, 'euro2020/assignedbidsperteam.html',
                  context={'league': currentleague.leaguename, 'teams': teams, 'bids': bids})


def rejectedbidsperteam(request, league):
    currentleague = League.objects.get(pk=league)
    teams = Team.objects.filter(league=currentleague).values()
    bids = Bids.objects.select_related('player').filter(team__in=list(teams.values_list()), assigned=False).order_by(
        '-playerbid')
    return render(request, 'euro2020/rejectedbidsperteam.html',
                  context={'league': currentleague.leaguename, 'teams': teams, 'bids': bids})


def unassignedplayersperleague(request, league):
    currentleague = League.objects.get(pk=league)
    teams = Team.objects.filter(league=currentleague).values()
    unassignedplayers = []
    players = Player.objects.all()
    assignedbids = Bids.objects.select_related('player').filter(team__in=list(teams.values_list()),
                                                                assigned=True).order_by(
        '-playerbid').values()
    for player in players:
        if not any(bid['player_id'] == player.id for bid in assignedbids):
            unassignedplayers.append(player)
    return render(request, 'euro2020/unassignedplayersperleague.html',
                  context={'league': currentleague.leaguename, 'players': unassignedplayers})


def leagueoverview(request):
    leagues = League.objects.all().order_by('leaguename')
    return render(request, 'euro2020/leagueoverview.html',
                  context={'leagues': leagues})


def leaguemanager(request, league):
    currentleague = League.objects.get(pk=league)
    return render(request, 'euro2020/leaguemanager.html',
                  context={'league': currentleague})


def teams(request, league):

    leagueteams = Team.objects.filter(league=league).order_by('name').select_related("owner")

    return render(request, 'euro2020/teams.html',
                  context={'leagueteams': leagueteams, 'leaguename': League.objects.get(pk=league).leaguename,
                           })


def lotingleague(request, league):
    error = ""
    drawlist = [["A", 1], ["A", 2], ["A", 3],["A", 4], ["B", 1], ["B", 2], ["B", 3],["B", 4], ["C", 1], ["C", 2], ["C", 3],["C", 4], ["D", 1], ["D", 2], ["D", 3], ["D", 4], ["E", 1], ["E", 2], ["E", 3],["E", 4], ["F", 1], ["F", 2], ["F", 3],["F", 4]]
    currentleague = League.objects.get(pk=league)
    leagueteams = Team.objects.filter(league=league).order_by('name').select_related("owner")
    if currentleague.draw == False:
        for team in leagueteams:
            print(drawlist)
            a = random.choice(drawlist)
            print(a[0])
            team.group = a[0]
            team.order = a[1]
            team.save()
            drawlist.remove(a)
        currentleague.draw = True
        currentleague.save()
    else:
        error = "Er heeft al een loting voor deze league plaatsgevonden"
        print(error)

    return render(request, 'euro2020/leaguemanager.html',
                  context={'league': currentleague})

def changephase(request, league):
    error = ""
    leaguename = League.objects.get(id=league).leaguename
    currentphase = League.objects.get(pk=league).gamephase
    nextgamephase = nextphase(currentphase)
    if request.method == 'POST':
        if request.POST.get("change"):
            obj = League.objects.get(pk=league)
            obj.gamephase = nextgamephase
            obj.save()
        return redirect(leaguemanager, league)

    return render(request, 'euro2020/changephase.html', context={'league': leaguename, 'currentphase': currentphase,
                                                                 'nextphase': nextgamephase.gamephase, "error": error})


def setupteams(request, league):
    currentuser = request.user
    if not currentuser.is_superuser:
        error = "You must be a super user to start the auction"
        return render(request, 'euro2020/leagueoverview.html',
                      context={'error': error})

    allteams = Team.objects.filter(league_id=league)
    if len(allteams) != 0:
        error = "This League already contains teams. To setup a League it should not contains teams"
        return redirect(leagueoverview)

    setup_teams(league)
    return redirect(leaguemanager, league)


def setupbids(request, league):
    currentuser = request.user
    if not currentuser.is_superuser:
        error = "You must be a super user to start the auction"
        return render(request, 'euro2020/assignedbidsperteam.html',
                      context={'bids': "", 'teams': "", 'error': error})

    currentleague = League.objects.get(pk=league)
    if not currentleague.gamephase.allowbidding:
        error = "The current game phase " + str(currentleague.gamephase) + " does not allow bids to be performed"
        return render(request, 'euro2020/assignedbidsperteam.html',
                      context={'bids': "", 'teams': "", 'error': error})

    prefix = currentleague.leaguename + "_"
    allleaguebids = Bids.objects.filter(team__name__istartswith=prefix, gamephase=currentleague.gamephase)
    if len(allleaguebids) != 0:
        error = "This League already contains bids for this phase. To setup bids for a League it should not contains bids"
        print(error)
        return redirect(leaguemanager, league)

    setup_bids(league, 202)
    return redirect(leagueoverview)


def deleteleaguedata(request, league):
    currentuser = request.user
    if not currentuser.is_superuser:
        error = "You must be a super user to start the auction"
        return redirect(leagueoverview)
    delete_league(league)
    return redirect(leagueoverview)


def createleague(request):
    currentuser = request.user
    error = ""
    if not currentuser.is_superuser:
        error = "You must be a super user to start the auction"
        return redirect(leagueoverview)

    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            namedata = form.cleaned_data
            leaguename = namedata.get('leaguename')

            # Eerst controleren of de op het formulier ingevoerde teamnaam al niet bestaat
            try:
                # Case insensitive check
                newleague = League.objects.get(leaguename__icontains=leaguename)
                if newleague:
                    error = "leagueexists"
                    return render(request, "euro2020/createleague.html",
                                  context={"form": CreateLeagueForm, "error": error})
            except:
                League.objects.create(leaguename=leaguename, maxparticipants=24, is_private=False,
                                      gamephase=GamePhase.objects.get(gamephase=nextphase(currentgamephase="01")))
            return redirect(leagueoverview)
        else:
            pass

    return render(request, "euro2020/createleague.html", context={"form": CreateLeagueForm, "error": error})


def regels(request):
    return render(request, "euro2020/regels.html")


def programma(request):
    return render(request, "euro2020/programma.html")


def moneymanager(request):
    error = ""
    allteams = Team.objects.all()
    allleagues = League.objects.all()
    if request.method == 'POST':
        if request.POST.get("boeking"):
            team = Team.objects.get(pk=request.POST['teamname1'])
            betcoins = int(request.POST['betcoins1'])
            team.betcoins += betcoins
            team.save()
            Boekhouding.objects.create(team=team, aantalbetcoins=betcoins, boekingsopmerking=request.POST['opmerking'])
            league = League.objects.get(pk=team.league_id)
            league.leaguebalance -= betcoins
            league.save()
            BoekhoudingLeague.objects.create(league=league, aantalbetcoins=-betcoins,
                                             boekingsopmerking=request.POST['opmerking'])
        elif request.POST.get("groepsfaseleague"):
            league = League.objects.get(leaguename=request.POST['leaguename'])
            leagueteams = Team.objects.filter(league=league)
            for eachteam in leagueteams:
                if eachteam.betcoins > 1000:
                    penalty = eachteam.betcoins - 1000
                    eachteam.betcoins -= penalty
                    eachteam.save()
                    comment = eachteam.name + " heeft te weinig betcoins uitgegeven in groepsfase. Gecorrigeerd naar 1000"
                    print(comment)
                    Boekhouding.objects.create(team=eachteam, aantalbetcoins=-penalty,
                                               boekingsopmerking=comment)
                    league.leaguebalance += penalty
                    league.save()
                    BoekhoudingLeague.objects.create(league=league, aantalbetcoins=penalty,
                                                     boekingsopmerking=comment)
                else:
                    print(
                        eachteam.name + " heeft te genoeg betcoins uitgegeven in groepsfase. NIET Gecorrigeerd naar 1000")
        elif request.POST.get("boekinginschrijving"):
            team = Team.objects.get(pk=request.POST['teamname'])
            betcoins = 2000
            team.betcoins += betcoins
            team.paid = True
            team.save()
            Boekhouding.objects.create(team=team, aantalbetcoins=betcoins,
                                       boekingsopmerking="Betaling ontvangen en verwerkt van team " + team.name)
            league = League.objects.get(pk=team.league_id)
            league.leaguebalance -= betcoins
            league.save()
            BoekhoudingLeague.objects.create(league=league, aantalbetcoins=-betcoins,
                                             boekingsopmerking="Betaling ontvangen en verwerkt van team " + team.name)
        else:
            error = "Er is op een onbekende knop gedrukt of een onbekende fout is opgetreden"
        return redirect(moneymanager)

    return render(request, "euro2020/moneymanager.html", context={"allteams": allteams, "allleagues": allleagues})


def tactiekopstelling(request):
    error = ""
    bidauction = False
    league = ""
    disabled = ""
    manager = request.user
    team = Team.objects.get(owner=manager)
    allgke = ""
    alldef = ""
    allmid = ""
    allatt = ""
    try:
        league = team.league
        leaguephase = league.gamephase
        if leaguephase.allowauction:
            disabled = "disabled"
        if leaguephase.allowbidding or leaguephase.allowauction:
            bidauction = True
    except:
        pass

    if request.method == 'POST':
        if request.POST.get("bewaarveiling"):
            team.bidbudget = request.POST['maxbetcoin']
            team.maxbidgke = request.POST['gke']
            team.maxbiddef = request.POST['def']
            team.maxbidmid = request.POST['mid']
            team.maxbidatt = request.POST['att']
            team.save()
            error = "Je instellingen zijn opgeslagen"
            return render(request, "euro2020/tactiekopstelling.html",
                          context={"allgke": allgke, "alldef": alldef, "allmid": allmid, "allatt": allatt,                                                                           "league": league,
                                    "bidauction": bidauction, "disabled": disabled, "team": team, "error": error})
        elif request.POST.get("bewaaropstelling"):
            team = Team.objects.get(pk=request.POST['teamname'])
        else:
            pass

    return render(request, "euro2020/tactiekopstelling.html",
                  context={"allgke": allgke, "alldef": alldef, "allmid": allmid, "allatt": allatt, "league": league,
                           "bidauction": bidauction, "disabled": disabled, "team": team, "error": error})


def groeprlmatches(request):
    allgroupmatches = Match.objects.filter(stage__startswith="G").order_by("start")
    allstages = Match.Stage

    # now = datetime.now(timezone.utc)
    # tournamentstarts = GameSettings.objects.get(gamesettings='tourstarttime').gamesettingsvalue
    # tourstarts = datetime.strptime(tournamentstarts, '%Y-%m-%d %H:%M:%S.%f')
    # tourstarts = tourstarts.astimezone(pytz.timezone("UTC"))
    # if now > tourstarts:
    #     print("Tournament has started")
    #     return True
    # else:
    #     print("Tournament has not started yet")
    #     return False

    groups = models.Country.Group.names
    return render(request, "euro2020/groeprlmatches.html",
                  context={"allgroupmatches": allgroupmatches, "allstages": allstages, "groups": groups})
