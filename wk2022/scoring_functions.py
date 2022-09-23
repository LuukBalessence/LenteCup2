from wk2022.models import Match, Goal, Country
from dataclasses import dataclass


@dataclass
class GroupStanding:
    """
    Dataclasses (https://docs.python.org/3/library/dataclasses.html) are classes that don't need
    functions but just hold data. They were added in Python 3.7 and this is a perfect use case for them.
    """

    country: Country
    GS: int = 0
    W: int = 0
    G: int = 0
    V: int = 0
    PT: int = 0
    DV: int = 0
    DT: int = 0
    PO: int = 0
    DF: int = 0
    POCOMMENT: str = ""


def getmatchlist(countries):
    matchlist = []
    for match in Match.objects.all():
        if (
            ((match.home in countries) and (match.away in countries))
            and (countries[match.home][0] == countries[match.away][0])
            and (match.has_ended)
        ):
            matchlist.append(match)
    return matchlist


def getgoallist(matches):
    goallist = []
    for goal in Goal.objects.all():
        if goal.match in matches:
            goallist.append(goal)
    return goallist


def match_results(wedstrijden, goals):
    results = {}
    # start with 0-0 for each match
    for wedstrijd in wedstrijden:
        results[wedstrijd] = [0, 0]

    # add goals
    for goal in goals:
        if (
            goal.player.country == goal.match.home and goal.type != Goal.Type.OWN_GOAL
        ) or (
            goal.player.country == goal.match.away and goal.type == Goal.Type.OWN_GOAL
        ):
            results[goal.match][0] += 1
        else:
            results[goal.match][1] += 1

    return results


def group_standings(results, countries):
    """
    We start with a dict where key=Country and value=GroupStanding (dataclass).
    We only need this dict while processing the standings.
    When we are done just return the values in a list.
    """
    standings = {}
    for country in countries:
        standings[country] = GroupStanding(country=country)
    # HG = HomeGoals, AG = AwayGoals
    for match, (HG, AG) in results.items():
        if match.stage not in [Match.Stage.G1, Match.Stage.G2, Match.Stage.G3]:
            continue

        if not match.has_ended:
            continue

        standings[match.home].GS += 1
        standings[match.away].GS += 1
        if HG > AG:
            standings[match.home].W += 1
            standings[match.home].PT += 3
            standings[match.away].V += 1
        elif HG < AG:
            standings[match.home].V += 1
            standings[match.away].W += 1
            standings[match.away].PT += 3
        else:  # draw
            standings[match.home].G += 1
            standings[match.home].PT += 1
            standings[match.away].G += 1
            standings[match.away].PT += 1

        standings[match.home].DV += HG
        standings[match.away].DV += AG
        standings[match.home].DT += AG
        standings[match.away].DT += HG
        standings[match.home].DF += (HG - AG)
        standings[match.away].DF += (AG - HG)

    # we don't need the key anymore, just return a list
    return list(standings.values())


def eufa_sort(groupstanding):
    """
    Niet alle regels worden op dit moment toegepast,
    bij gelijke stand geldt onderling resultaat is redelijk lastig te maken
    dus die implementatie volgt als blijkt dat het echt nodig is.
    Tot die tijd is het mogelijk om (in de admin) de order van een land binnen de
    groep aan te passen zodat we altijd zelf kunnen bepalen wat de volgorde is als
    alle andere waarden gelijk zijn.
    De punten etc. worden vermenigvuldigd met -1 om de sortering goed te houden.
    """
    return (
        groupstanding.country.group,  # group
        # groupstanding.GS * -1, # Matches played
        groupstanding.PT * -1,
        groupstanding.PO,  # position
        # eval("groupstanding." + rank),  # Position after each
        # (groupstanding.DV - groupstanding.DT) * -1,  # goal difference
        # groupstanding.DV * -1,  # scored goals
        # groupstanding.W * -1,  # matches won
        # groupstanding.country.order,  # arbitrary country ordering
    )


def equalityofpoints(groupstandings, property, zero):
    currentgroup = ""
    first_iter = True
    countries = {}
    for group in Country.Group:
        currentgroup = group
        num = 0
        for stand in groupstandings:
            if group == stand.country.group:
                num += 1
                stand.PO = num
                #s2 = eval("s1." + property)
                if not first_iter:
                    if (
                       ((eval("s1." + property)) == (eval("stand." + property)))
                        and (s1.GS == stand.GS)
                        and ((stand.GS != 0) or zero)
                        and (not first_iter)
                    ):
                        stand.POCOMMENT = (
                            "equal" + property + str(eval("stand." + property))
                        )
                        s1.POCOMMENT = "equal" + property + str(eval("s1." + property))
                        if not stand.country in countries:
                            countries.setdefault(stand.country, [stand.POCOMMENT, stand.PO])
                        if not s1.country in countries:
                            countries.setdefault(s1.country, [s1.POCOMMENT, s1.PO])
                    s1 = stand
                else:
                    s1 = stand
                    first_iter = False
    return countries

def recalculateposition(overallstandings, stand1):
    equalstring = ""
    equalgroup = ""
    for standing in overallstandings:
        if standing.POCOMMENT.startswith("equal"):
            if (standing.country.group != equalgroup) or (standing.POCOMMENT != equalstring):
                order = 1
            standing.PO = standing.PO + stand1[standing.country][1] - order
            equalstring = standing.POCOMMENT
            equalgroup = standing.country.group
            order += 1
    return overallstandings


if __name__ == "__main__":
    results = match_results(Match.objects.all(), Goal.objects.all())
    standings = group_standings(results, Country.objects.all())
    standings.sort(key=eufa_sort)
    #equalityofpoints(standings, Country.objects.all())
