from euro2020.models import Player, Bids, Team, League
import random


def createbidlist(currentteam, country_name):
    initialbids = []
    teamexistingbids = Bids.objects.filter(team=currentteam).values()
    players = Player.objects.filter(country__name=country_name).order_by('country', 'position')
    for player in players:
        # We moeten hier de playername toch definieren omdat anders de initialbid niet overeenkomt met de
        # cleaned data structuur
        # Voorbeelden van de initialbid voor een speler en de form_cleaned data
        # {'player': <Player: Kevin Lasagna>, 'playerpk': '755', 'position': 'A', 'bid': 8}
        # {'position': 'A', 'player': 'Kevin Lasagna', 'playerpk': '755', 'bid': 8}
        playername = player.first_name + " " + player.last_name
        try:
            currentbid = teamexistingbids.get(player_id=player.id, team=currentteam)
            initialbids.append(
                {"player": playername, "playerpk": str(player.id),
                 "position": player.position, "bid": currentbid["playerbid"]})
            # print(currentbid['playerbid'])
        except:
            initialbids.append(
                {"player": playername, "playerpk": str(player.id), "position": player.position, "bid": None})
    return initialbids


def validbid(bid, team, players):
    # Als de bieding aan 1 van onderstaande 4 voorwaarden voldoet is dit geen geldige bieding
    # 1 Het geboden bedrag is hoger dan het budget van de betreffende manager
    # 2 De manager heeft al 20 voetballers toegewezen gekregen
    # 3 Het maximum aantal voetballers(3,8 of 5) van de betreffende positie is al toegewezen aan de manager
    # 4 Het door de manager zelf opgegeven maximum aantal voetballers in deze veilingronde van de
    # betreffende linie is al toegewezen aan de manager

    if bid['playerbid'] > team['betcoins']:
        return [False, "REJECTION 1a: Not enough betcoins(" + str(team['betcoins']) + ") to buy this player"]
    if bid['playerbid'] > team['bidbudget']:
        return [False, "REJECTION 1b: Not enough budget in this phase(" + str(team['betcoins']) + ") to buy this player"]

    teamcount = team['gkecount'] + team['defcount'] + team['midcount'] + team['attcount']
    if teamcount >= 20:
        return [False, "REJECTION 2: You have reached the maximum of 20 players"]
    player = list(filter(lambda x: x['id'] == bid['player_id'], players))[0]
    position = player['position']
    if position == 'G' and team['gkecount'] == 3:
        return [False, "REJECTION 3a: You have reached the maximum of 3 goalkeepers for your team"]
    elif position == 'G' and team['budgetgkecount'] == team['maxbidgke']:
        return [False, "REJECTION 3b: You have reached your maximum configured goalkeepers to buy for this phase "]
    elif position == 'D' and team['defcount'] == 8:
        return [False, "REJECTION 4a: You have reached the maximum of 8 defenders for your team"]
    elif position == 'D' and team['budgetdefcount'] == team['maxbiddef']:
        return [False, "REJECTION 4b: You have reached your maximum configured defenders to buy for this phase "]
    elif position == 'M' and team['midcount'] == 8:
        return [False, "REJECTION 5a: You have reached the maximum of 8 midfielders for your team"]
    elif position == 'M' and team['budgetmidcount'] == team['maxbidmid']:
        return [False, "REJECTION 5b: You have reached your maximum configured midfielders to buy for this phase "]
    elif position == 'A' and team['attcount'] == 5:
        return [False, "REJECTION 6a: You have reached the maximum of 5 attackers for your team"]
    elif position == 'A' and team['budgetattcount'] == team['maxbidatt']:
        return [False, "REJECTION 6b: You have reached your maximum configured attackers to buy for this phase "]

    # TODO Implement max player position entered by manager
    # TODO Use budget maximum entered by manager
    return [True, "Valid bid"]


def savebid(bid, assigned, bidcomment, team, players):
    bid['assigned'] = assigned
    bid['bidcomment'] = bidcomment
    obj = Bids.objects.get(id=bid['id'])
    obj.assigned = assigned
    obj.bidcomment = bidcomment
    obj.save()
    # Als een speler wordt toegewezen, dienen een aantal warades te worden aangepast: Het huidige saldo, het biedsaldo,
    # het leagua saldo, de positieteller, de beidingspositieteller
    if assigned == True and not team == "":
        currentbalance = team['betcoins']
        newbalance = currentbalance - bid['playerbid']
        team['betcoins'] = newbalance
        currentbudget = team['bidbudget']
        newbudget = currentbudget - bid['playerbid']
        team['bidbudget'] = newbudget
        league = League.objects.get(pk = team['league_id'])
        league.leaguebalance += bid['playerbid']
        league.save()
        player = list(filter(lambda x: x['id'] == bid['player_id'], players))[0]
        position = player['position']
        if position == 'G':
            team['gkecount'] += 1
            team['budgetgkecount'] += 1
        elif position == 'D':
            team['defcount'] += 1
            team['budgetdefcount'] += 1
        elif position == 'M':
            team['midcount'] += 1
            team['budgetmidcount'] += 1
        elif position == 'A':
            team['attcount'] += 1
            team['budgetattcount'] += 1
    return [bid, team]


def saveteaminfo(teams):
    for team in teams:
        obj = Team.objects.get(id=team['id'])
        obj.betcoins = team['betcoins']
        obj.save()


def assignfinalbid(bidlist, teamlist, players):
    # Deze functie wordt alleen aangeroepen voor valide biedingen
    # Als er 1 bieding in de bidlist is: Verwerk deze bieidng en geef de bieding terug
    if len(bidlist) == 1:
        bid = bidlist[0]
        print(bid)
        print(teamlist)
        result = savebid(bid, True, "ASSIGNED 01: Highest bid", teamlist[0], players)
        return result

    # Er zijn meer resultaten met dezelfde bieding.
    # Indien er twee of meer hoogste biedingen zijn op dezelfde voetballer dan wordt de volgorde
    # bepaald op de volgende manier:
    # 1 Het bod van de manager met het laagste aantal toegewezen voetballers komt bovenaan.
    # 2 Indien dit gelijk is komt het bod van de manager met het tot dan toe minst uitgegeven bedrag (het hoogste budget) bovenaan
    # 3 Indien dit ook gelijk is wordt er geloot
    # 4 Indien er 1 team uiteindelijk meerdere dezelfde biedingen heeft wordt de eerste bieding toegewezen

    # We bepalen het minimum aantal spelers in de teamlijst. Daarna kijken we welke teams hieraan voldoen.
    # De rest halen we uit de teamlijst
    minimumcount = min([(x['gkecount'] + x['defcount'] + x['midcount'] + x['attcount']) for x in teamlist])
    for team in teamlist[::-1]:
        count = team['gkecount'] + team['defcount'] + team['midcount'] + team['attcount']
        if count == minimumcount:
            pass
        else:
            teamlist.remove(team)

    # Als er 1 team over is: Zoek een bieding uit de bidlist bij dit team, werk de biedlijst bij en geef de bieding terug
    if len(teamlist) == 1:
        bid = list(filter(lambda x: x['team_id'] == teamlist[0]['id'], bidlist))[0]
        result = savebid(bid, True, "ASSIGNED 02: Highest equal bid but with the least players in the squad",
                teamlist[0], players)
        return result

    # Als er meer teams zijn overgebleven gaan we kijken wie er nog het meeste totale budget heeft.
    else:
        maxbudget = max([x['betcoins'] for x in teamlist])
        for x in teamlist[::-1]:
            if not x['betcoins'] == maxbudget:
                teamlist.remove(x)

        # Als er 1 bieding over is: Zoek een bieding uit de bidlist bij dit team, werk de biedlijst bij en geef de bieding terug
        if len(teamlist) == 1:
            for bid in bidlist:
                if bid['team_id'] == teamlist[0]['id']:
                    result = savebid(bid, True, "ASSIGNED 03: Highest equal bid but with higher budget", teamlist[0], players)
                    return result
        # Als er meer teams zijn overgebleven met even weinig spelers en een even hoog budget gaan we loten
        else:
            winningteam = ""
            maxnumber = 0
            for team in teamlist:
                x = random.random()
                if x > maxnumber:
                    winningteam = team
                    maxnumber = x
            # Selecteer de eerste beiding van het winnende team.
            for bid in bidlist:
                if bid['team_id'] == winningteam['id']:
                    result = savebid(bid, True, 'ASSIGNED 04: Highest equal bid, but with highest random number.', winningteam,
                    players)
                    return result
    print("Hier mogen we nooit komen")


def remove_sameplayer_bids(bids, player, teams):
    for bid in bids[::-1]:
        if bid['player_id'] == player:
            team = list(filter(lambda x: x['id'] == bid['team_id'], teams))
            savebid(bid, False, "REJECTED 00: Not the highest bid", team, "")
            bids.remove(bid)
    return bids

