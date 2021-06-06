from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("groepstand", views.groepstand, name="groepstand"),
    path("standenbeheer", views.standenbeheer, name="standenbeheer"),
    path("euro2020", views.euro2020, name="euro2020"),
    path("match/<int:pk>/add_goal", views.add_goal, name="add-goal"),
    path("changeteamname", views.changeteamname, name="changeteamname"),
    path("changefirstname", views.changefirstname, name="changefirstname"),
    path("pickleague", views.pickleague, name="pickleague"),
    path("myteam", views.myteam, name="myteam"),
    path("bids", views.bids, name="bids"),
    path("bidoverview", views.bidoverview, name="bidoverview"),
    path("listallbids", views.listallbids, name="listallbids"),
    path("bids/<str:country_name>", views.bids, name="bidspercountry"),
    path("assignedbidsperteam/<int:league>", views.assignedbidsperteam, name="assignedbidsperteam"),
    path("rejectedbidsperteam/<int:league>", views.rejectedbidsperteam, name="rejectedbidsperteam"),
    path("unassignedplayersperleague/<int:league>", views.unassignedplayersperleague, name="unassignedplayersperleague"),
    path("auction/<int:league>/<str:gamephase>", views.auction, name="auction"),
    path("minplayerpositions/<int:league>", views.minplayerpositions, name="minplayerpositions"),
    path("fillteams/<int:league>", views.fillteams, name="fillteams"),
    path("initiallineup/<int:league>", views.initiallineup, name="initiallineup"),
    path("leaguemanager/<int:league>", views.leaguemanager, name="leaguemanager"),
    path("leagueoverview", views.leagueoverview, name="leagueoverview"),
    path("teams/<int:league>", views.teams, name="teamsperleague"),
    path("livescoring", views.livescoring, name="livescoring"),
    path("lotingleague/<int:league>", views.lotingleague, name="lotingleague"),
    path("changephase/<int:league>", views.changephase, name="changephase"),
    path("setupteams/<int:league>", views.setupteams, name="setupleagueteams"),
    path("setupbids/<int:league>", views.setupbids, name="setupleaguebids"),
    path("deleteleaguedata/<int:league>", views.deleteleaguedata, name="deleteleaguedata"),
    path("createleague", views.createleague, name="createleague"),
    path("regels", views.regels, name="regels"),
    path("programma", views.programma, name="programma"),
    path("myleague", views.myleague, name="myleague"),
    path("leaguestand/<int:league>", views.leaguestand, name="leaguestand"),
    path("createleaguematches/<int:league>", views.createleaguematches, name="createleaguematches"),
    path("rleuro2020", views.rleuro2020, name="rleuro2020"),
    path("groeprlmatches", views.groeprlmatches, name="groeprlmatches"),
    path("moneymanager", views.moneymanager, name="moneymanager"),
    path("tactiekopstelling", views.tactiekopstelling, name="tactiekopstelling"),
    path("myledger", views.myledger, name="myledger"),
    path("hulpbieden", views.hulpbieden, name="hulpbieden"),
]
