from django.shortcuts import redirect, render

from LenteCup2.models import GameSettings
from common.models import AppAuthorisation, Apps
from .forms import AanmeldForm, ScumForm
from .models import GolfProfiel, BaanProfiel, GolfBaanProfiel, Hole, Flight, Scum


def home(request):
    try:
        currentuser = request.user
        return render(request, 'luukopen21/usermenu.html')
    except:
        error = "You are not logged in, Please login or create an account"
        return redirect(to="home")


def usermenu(request):
    startscum = False
    show = GameSettings.objects.get(gamesettings='scumstarted').gamesettingsvalue
    if show == "True":
        startscum = True
    return render(request, 'luukopen21/usermenu.html', {'startscum': startscum})


def donderdag(request):
    return render(request, 'luukopen21/donderdag.html')


def vrijdag(request):
    return render(request, 'luukopen21/vrijdag.html')


def zaterdag(request):
    return render(request, 'luukopen21/zaterdag.html')


def zondag(request):
    return render(request, 'luukopen21/zondag.html')


def aanmelden(request):
    startscum = False
    show = GameSettings.objects.get(gamesettings='scumstarted').gamesettingsvalue
    if show == "True":
        startscum = True
    currentapp = Apps.objects.get(appname="Luuk Open 2021")
    currentuser = request.user
    if len(AppAuthorisation.objects.filter(user=currentuser.id, app=currentapp)) == 1:
        return redirect(usermenu)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AanmeldForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            formdata = form.cleaned_data
            # Als de gebruiker zich nog niet heeft ingeschreven, dan verwerken we de data en maken we een autorisatatie
            if len(AppAuthorisation.objects.filter(app=currentapp.id, user=currentuser)) == 0:
                AppAuthorisation.objects.create(app=currentapp, user=currentuser)
                GolfProfiel.objects.create(naam=formdata['naam'], ehcp=formdata['ehcp'],
                                           opmerking=formdata['opmerking'],
                                           eigenaar=currentuser, buggy=formdata['buggy'], huurset=formdata['huurset'],
                                           preluukopen=formdata['preluukopen'])
            deelnemers = GolfProfiel.objects.all()
            return render(request, 'luukopen21/lijstaanmeldingen.html', {'deelnemers': deelnemers, 'startscum': startscum})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AanmeldForm()

    return render(request, 'luukopen21/aanmelden.html', {'form': form, 'startscum': startscum})


def lijstaanmeldingen(request):
    deelnemers = GolfProfiel.objects.all().order_by('-totalscore')
    return render(request, 'luukopen21/lijstaanmeldingen.html', {'deelnemers': deelnemers})


def praktischeinfo(request):
    return render(request, 'luukopen21/praktischeinfo.html')


def scumofthegolfcourse(request):
    return render(request, 'luukopen21/scumofthegolfcourse.html')


def preluukopen(request):
    flights = Flight.objects.filter(
        naam__in=['Lage Vuursche Flight 1', 'Lage Vuursche Flight 2', 'Lage Vuursche Flight 3'])
    return render(request, 'luukopen21/preluukopen.html', context={'flights': flights})


def golfbaaninfo(request):
    golfbaanprofielen = GolfBaanProfiel.objects.all()
    deelnemer = GolfProfiel.objects.get(eigenaar=request.user)
    return render(request, 'luukopen21/golfbaaninfo.html',
                  {'deelnemer': deelnemer, 'golfbaanprofielen': golfbaanprofielen})


def speldo1(request):
    flights = Flight.objects.filter(
        naam__in=['Golf4All Flight 1', 'Golf4All Flight 2', 'Golf4All Flight 3', 'Golf4All Flight 4'])
    return render(request, 'luukopen21/speldo1.html', context={'flights': flights})


def heather(request):
    flights = Flight.objects.filter(
        naam__in=['Ullerberg Flight 1', 'Ullerberg Flight 2', 'Ullerberg Flight 3', 'Ullerberg Flight 4'])
    return render(request, 'luukopen21/heather.html', context={'flights': flights})


def clubsblack(request):
    flights = Flight.objects.filter(
        naam__in=['Zeewolde Flight 1', 'Zeewolde Flight 2', 'Zeewolde Flight 3', 'Zeewolde Flight 4'])
    return render(request, 'luukopen21/clubsblack.html', context={'flights': flights})


def blackmystery(request):
    flights = Flight.objects.filter(
        naam__in=['StrandHorst Flight 1', 'StrandHorst Flight 2', 'StrandHorst Flight 3', 'StrandHorst Flight 4'])
    return render(request, 'luukopen21/blackmystery.html', context={'flights': flights})


def foursomes(request):
    flights = Flight.objects.filter(
        naam__in=['Nunspeet1 Flight 1', 'Nunspeet1 Flight 2', 'Nunspeet1 Flight 3', 'Nunspeet1 Flight 4'])
    return render(request, 'luukopen21/foursomes.html', context={'flights': flights})


def fourballs(request):
    flights = Flight.objects.filter(
        naam__in=['Nunspeet2 Flight 1', 'Nunspeet2 Flight 2', 'Nunspeet2 Flight 3', 'Nunspeet2 Flight 4'])
    return render(request, 'luukopen21/fourballs.html', context={'flights': flights})


def singles(request):
    flights = Flight.objects.filter(
        naam__in=['Nunspeet3 Flight 1', 'Nunspeet3 Flight 2', 'Nunspeet3 Flight 3', 'Nunspeet3 Flight 4'])
    return render(request, 'luukopen21/singles.html', context={'flights': flights})


def halvefinale(request):
    flights = Flight.objects.filter(
        naam__in=['Scherp1 Flight 1', 'Scherp1 Flight 2', 'Scherp1 Flight 3', 'Scherp1 Flight 4'])
    return render(request, 'luukopen21/halvefinale.html', context={'flights': flights})


def finale(request):
    flights = Flight.objects.filter(
        naam__in=['Scherp2 Flight 1', 'Scherp2 Flight 2', 'Scherp2 Flight 3', 'Scherp2 Flight 4'])
    return render(request, 'luukopen21/finale.html', context={'flights': flights})


def scumadmin(request):
    deelnemers = len(GolfProfiel.objects.filter(verradergame=True))
    golfscum = len(GolfProfiel.objects.filter(verradergame=True, verraders=True))
    golfers = len(GolfProfiel.objects.filter(verradergame=True, verraders=False))
    return render(request, 'luukopen21/scumadmin.html',
                  {'deelnemers': deelnemers, 'golfscum': golfscum, 'golfers': golfers})


def sogidentiteit(request):
    error = ""
    currentuser = request.user
    currentgolfer = GolfProfiel.objects.get(eigenaar=currentuser.id)
    deelnemers = GolfProfiel.objects.filter(verradergame=True)
    if currentgolfer.verraders:
        if request.method == 'POST':
            form = ScumForm(request.POST)
            naam1 = request.POST.get('stemweg1')
            naam2 = request.POST.get('stemweg2')
            Scum.objects.all().delete()
            Scum.objects.create(naam=naam1)
            Scum.objects.create(naam=naam2)
            return redirect(gelukt)

    return render(request, 'luukopen21/sogidentiteit.html', {'currentgolfer': currentgolfer, 'deelnemers': deelnemers})


def gelukt(request):
    scums = Scum.objects.all()
    return render(request, 'luukopen21/gelukt.html', {'scums': scums})


def showelims(request):
    visible = False
    show = GameSettings.objects.get(gamesettings='Gelukt').gamesettingsvalue
    if show == "True":
        visible = True
    scums = Scum.objects.all()
    return render(request, 'luukopen21/showelims.html', {'scums': scums, 'visible': visible})
