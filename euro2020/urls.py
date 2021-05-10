from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("groepstand", views.groepstand, name="groepstand"),
    path("standenbeheer", views.standenbeheer, name="standenbeheer"),
    path("euro2020", views.euro2020, name="euro2020"),
    path("match/<int:pk>/add_goal", views.add_goal, name="add-goal"),
    path("myaccount", views.myaccount, name="myaccount"),
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
    path("leaguemanager/<int:league>", views.leaguemanager, name="leaguemanager"),
    path("leagueoverview", views.leagueoverview, name="leagueoverview"),
    path("teams/<int:league>", views.teams, name="teamsperleague"),
    path("changephase/<int:league>", views.changephase, name="changeleaguephase"),
    path("setupteams/<int:league>", views.setupteams, name="setupleagueteams"),
    path("setupbids/<int:league>", views.setupbids, name="setupleaguebids"),
    path("deleteleaguedata/<int:league>", views.deleteleaguedata, name="deleteleaguedata"),
    path("createleague", views.createleague, name="createleague"),
]