from django.shortcuts import redirect, render
from common.models import AppAuthorisation, Apps
from .forms import AanmeldForm
from .models import GolfProfiel

def home(request):
    try:
        currentuser = request.user
        return render(request, 'luukopen21/usermenu.html')
    except:
        error = "You are not logged in, Please login or create an account"
        return redirect(to="home")


def usermenu(request):
    return render(request, 'luukopen21/usermenu.html')


def donderdag(request):
    return render(request, 'luukopen21/donderdag.html')


def vrijdag(request):
    return render(request, 'luukopen21/vrijdag.html')


def zaterdag(request):
    return render(request, 'luukopen21/zaterdag.html')


def zondag(request):
    return render(request, 'luukopen21/zondag.html')


def aanmelden(request):
    currentapp = Apps.objects.get(appname="Luuk Open 2021")
    currentuser = request.user
    if len(AppAuthorisation.objects.filter(user=currentuser.id, app=currentapp)) == 1:
        return render(request, 'luukopen21/usermenu.html')
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
                GolfProfiel.objects.create(naam=formdata['naam'], ehcp=formdata['ehcp'],opmerking=formdata['opmerking'],
                                           eigenaar=currentuser, buggy=formdata['buggy'], huurset=formdata['huurset'],preluukopen=formdata['preluukopen'])
            deelnemers = GolfProfiel.objects.all()
            return render(request, 'luukopen21/lijstaanmeldingen.html', {'deelnemers': deelnemers})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AanmeldForm()

    return render(request, 'luukopen21/aanmelden.html', {'form': form})

def lijstaanmeldingen(request):
    deelnemers = GolfProfiel.objects.all().order_by('-totalscore')
    return render(request, 'luukopen21/lijstaanmeldingen.html', {'deelnemers': deelnemers})

def praktischeinfo(request):
    return render(request, 'luukopen21/praktischeinfo.html')


def scumofthegolfcourse(request):
    return render(request, 'luukopen21/scumofthegolfcourse.html')

def preluukopen(request):
    return render(request, 'luukopen21/preluukopen.html')

def speldo1(request):
    return render(request, 'luukopen21/speldo1.html')

def heather(request):
    return render(request, 'luukopen21/heather.html')

def clubsblack(request):
    return render(request, 'luukopen21/clubsblack.html')

def blackmystery(request):
    return render(request, 'luukopen21/blackmystery.html')

def foursomes(request):
    return render(request, 'luukopen21/foursomes.html')

def fourballs(request):
    return render(request, 'luukopen21/fourballs.html')

def singles(request):
    return render(request, 'luukopen21/singles.html')

def halvefinale(request):
    return render(request, 'luukopen21/halvefinale.html')

def finale(request):
    return render(request, 'luukopen21/finale.html')

