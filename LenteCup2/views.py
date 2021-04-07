from datetime import datetime
from django.shortcuts import render, redirect

from LenteCup2.forms import ChangeFirstNameForm, ScoresForm, GekozenSpelersForm
from LenteCup2.models import Week, Scores, Speler, GekozenSpelers
from common.models import User
from collections import OrderedDict

def home(request):
    return render(request, "LenteCup/home.html", )


def explain(request):
    return render(request, "LenteCup/explain.html", )


def about(request):
    return render(request, "LenteCup/about.html", )


def myaccount(request):
    manager = request.user

    try:
        firstname = request.user.first_name
    except:
        firstname = ""

    return render(
        request=request,
        template_name="LenteCup/myaccount.html",
        context={"manager": manager, "firstname": firstname})


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
            return render(request, "LenteCup/changefirstname.html", {'form': ChangeFirstNameForm})

    else:
        return render(request, template_name="LenteCup/changefirstname.html")


def recalculate_week_scores(week, qualifying, currentuser):
    if qualifying == 'False':
        obj = Scores.objects.get(week_id=week, user=currentuser)
        obj.finalscore = 1.00
        obj.save()
    else:
        maxpoints = Week.objects.get(week=week).maxpoints
        getpoints = True
        currentscore = -1
        qualifyingscores = Scores.objects.filter(week_id=week, qualifying=qualifying).order_by('-score').values()
        totalscores = len(qualifyingscores)
        totalitems = 0
        amount = len(qualifyingscores)
        for x in range(0, totalscores):
            # Als de stableford score dezelfde is als de vorige score, worden dezelfde punten uitgedeeld als de vorige score heeft gehad.
            if currentscore == qualifyingscores[x]['score']:
                obj = Scores.objects.get(pk=qualifyingscores[x]['id'])
                obj.finalscore = pointstoscore
                obj.save()
            # Als de stableford score de eerste score is of anders dan voorgaande stbf-score, wordt het aantal uit te delen punten bepaald.
            # Dit gebeurt alleen als alle punten al niet vergeven zijn.
            else:
                if not getpoints:
                    qualifyingscores[x]['finalscore'] = 1
                    obj = Scores.objects.get(pk=qualifyingscores[x]['id'])
                    obj.finalscore = 1.00
                    obj.save()

                else:
                    currentscore = qualifyingscores[x]['score']
                    totalitems = len([d for d in qualifyingscores if d.get('score') == currentscore])
                    if maxpoints - x - totalitems == 1:
                        pointstoscore = maxpoints - x - (totalitems - 1)*0.5
                        getpoints = False
                    if maxpoints - x - totalitems > 1:
                        pointstoscore = maxpoints - x - (totalitems - 1)*0.5
                    if maxpoints - x - totalitems < 1:
                        total=0
                        getpoints = False
                        for y in range((maxpoints - x - totalitems), (maxpoints - x )):
                            if (y + 1) <= 1:
                                total += 1
                            else:
                                total = total + y + 1
                        pointstoscore = total / totalitems
                    obj = Scores.objects.get(pk=qualifyingscores[x]['id'])
                    obj.finalscore = pointstoscore
                    obj.save()
    return


def standinvoer(request):
    error=""
    currentuser = request.user
    manager = currentuser.first_name
    weeksopen = Week.objects.filter(openforscoring=True)
    form = ScoresForm(request.GET)
    if manager == "":
        error = "Je hebt nog geen naam geregistreerd. Ga naar je profiel en vul je naam"
        print(error)
        return render(request, "LenteCup/standinvoer.html",
                      {'form': form, 'weeksopen': weeksopen, 'manager': manager, 'error': error})
    if request.method == 'POST':
        form = ScoresForm(request.POST)
        if form.is_valid():
            if request.POST['weekname'] == "" or request.POST['qualifying'] == "":
                error = "Je hebt geen week of qualifying keuze ingevuld"
                print(error)
                return render(request, "LenteCup/standinvoer.html",
                              {'form': form, 'weeksopen': weeksopen, 'manager': manager, 'error': error})
            week_id = Week.objects.get(week=request.POST['weekname'])
            try:
                obj = Scores.objects.get(user=currentuser, week=week_id)
                obj.score = int(request.POST['score'])
                obj.qualifying = request.POST['qualifying']
                obj.baan = request.POST['baan']
                obj.lus = request.POST['lus']
                obj.save()
                message = "Updated your weekscore"
                print(message)
            except:
                obj1 = Scores.objects.create(
                    user=currentuser, week=week_id, score=int(request.POST['score']),
                    qualifying=request.POST['qualifying'], baan=request.POST['baan'],
                    lus=request.POST['lus'])
                obj1.save()
            recalculate_week_scores(week_id, request.POST['qualifying'], currentuser)
            return redirect(to="jouwuitslagen")
        else:
            return render(request, "LenteCup/standinvoer.html",
                          {'form': form, 'weeks': weeksopen, 'manager': manager, 'error': error})
    else:
        return render(request, "LenteCup/standinvoer.html",
                      {'form': form, 'weeksopen': weeksopen, 'manager': manager})


def jouwuitslagen(request):
    currentuser = request.user
    scores = Scores.objects.filter(user=currentuser)
    return render(request, "LenteCup/jouwuitslagen.html",
                          {'scores': scores})

def overallstandlc(request):
    allusers = User.objects.all()
    tempscore = []
    for everyuser in allusers:
        userscores = Scores.objects.filter(user=everyuser)
        totalscore=0
        for everyscore in userscores:
            totalscore = totalscore + everyscore.finalscore
        if totalscore == 0:
            totalscore = 0.00
        tempscore += [[everyuser.first_name, totalscore]]
    sorted_score = OrderedDict()
    for username, score in sorted(tempscore, key=lambda x: x[1], reverse=True):
        sorted_score[username] = score
    return render(request, "LenteCup/overallstandlc.html",
                  {'scores': sorted_score})


def weekuitslagen(request):
    tempscore = []
    sorted_score = OrderedDict()
    weeks = Week.objects.all()
    userscores = Scores.objects.all().select_related('week')
    # for eachscore in userscores:
    #     tempscore += [[eachscore.user.first_name, eachscore.finalscore]]
    # for username, score in sorted(tempscore, key=lambda x: x[1], reverse=True):
    #     sorted_score[username] = score
    return render(request, "LenteCup/weekuitslagen.html",
                  {'scores': userscores,'weeks': weeks})


def spelerslijst(request):
    spelers= Speler.objects.all()
    return render(request, "LenteCup/spelerslijst.html",
                  {'spelers': spelers})


def tournamentstarted():
    now = datetime.now()
    tournamentstarts = datetime(2021, 4, 8, 12, 1, 59, 342380)
    # tournamentstarts = datetime(2021, 4, 8, 12, 1, 59, 342380)
    if now > tournamentstarts:
        print("Tournament has started")
        return True
    else:
        print("Tournament has not started yet")
        return False


def kiesspelers(request):
    error = ""
    currentuser = request.user
    manager = currentuser.first_name
    spelers = Speler.objects.all()
    form = GekozenSpelersForm(request.GET)
    if manager == "":
        error = "Je hebt nog geen naam geregistreerd. Ga naar je profiel en vul je naam"
        print(error)
        return render(request, "LenteCup/kiesspelers.html",
                      {'form': form, 'spelers': spelers, 'manager': manager, 'error': error})
    if tournamentstarted():
        return redirect(to="jouwspelers")
    if request.method == 'POST':
        GekozenSpelers.objects.filter(user=currentuser).delete()
        form = GekozenSpelersForm(request.POST)
        if form.is_valid():
            check = True
            playerlist = []
            for i in range (1,11):
                selectbox = 'plaats' + str(i)
                if request.POST[selectbox] == "":
                    error = "Je hebt in ieder geval voor plaats " + str(i) + " niets ingevuld"
                    print(error)
                    check = False
                    break
                else:
                    if any(request.POST[selectbox] in sublist for sublist in playerlist):
                        dubbele = Speler.objects.get(pk=int(request.POST[selectbox]))
                        error = "Je hebt de speler " + dubbele.first_name + " " + dubbele.last_name + " meerdere keren ingevoerd"
                        print(error)
                        check = False
                        break
                    else:
                        playerlist += [[manager, request.POST[selectbox]]]
            if check:
                for j in range(1, 11):
                    gekozenspeler = Speler.objects.get(pk=int(playerlist[j-1][1]))
                    try:
                        obj = GekozenSpelers.objects.get(speler=gekozenspeler, user=currentuser)
                        obj.user = currentuser
                        obj.speler = gekozenspeler
                        obj.eindplaats = j
                        obj.save()
                    except:
                        obj1 = GekozenSpelers.objects.create(user=currentuser, speler=gekozenspeler, eindplaats=j)
                        obj1.save()
                return redirect(to="jouwspelers")
            else:
                return render(request, "LenteCup/kiesspelers.html",
                              {'form': form, 'spelers': spelers, 'manager': manager, 'error': error})
        else:
            return render(request, "LenteCup/kiesspelers.html",
                          {'form': form, 'spelers': spelers, 'manager': manager, 'error': "er ging iets mis met het formulier"})
    else:
        return render(request, "LenteCup/kiesspelers.html",
                      {'form': form, 'spelers': spelers, 'manager': manager, "range": range(10)})


def jouwspelers(request):
    currentuser = request.user
    gekozenspelers = GekozenSpelers.objects.filter(user=currentuser).select_related('speler').order_by('eindplaats')
    if tournamentstarted():
        message = "De Masters is gestart, Jouw golfers zijn niet meer aan te passen"
    else:
        message = "De Masters is nog niet gestart, Je kunt je golfers nog wijzigen."
    return render(request, "LenteCup/jouwspelers.html",
                  {'gekozenspelers': gekozenspelers, 'message': message})


def huidigestand(request):
    users = User.objects.all()
    masterresults = Speler.objects.filter(position__isnull=False)
    userresults = []
    if tournamentstarted():
        for user in users:
            totalscore = 0
            userscores = GekozenSpelers.objects.filter(user=user)
            if len(userscores) == 0:
                pass
            else:
                for score in userscores:
                    total = 0
                    if score.speler in masterresults:
                        total = 5
                        totalscore += 5
                        masterresult = masterresults.filter(first_name=score.speler.first_name, last_name=score.speler.last_name).get().position
                        if score.eindplaats == masterresult:
                            if masterresult == 1:
                                total += 30
                                totalscore += 30
                            if masterresult == 2:
                                total += 18
                                totalscore += 18
                            if masterresult == 3:
                                total += 16
                                totalscore += 16
                            if masterresult == 4:
                                total += 7
                                totalscore += 7
                            if masterresult == 5:
                                total += 6
                                totalscore += 6
                            if masterresult == 6:
                                total += 5
                                totalscore += 5
                            if masterresult == 7:
                                total += 4
                                totalscore += 4
                            if masterresult == 8:
                                total += 3
                                totalscore += 3
                            if masterresult == 9:
                                total += 2
                                totalscore += 2
                            if masterresult == 10:
                                total += 1
                                totalscore += 1
                    obj = score
                    obj.punten = total
                    obj.save()
                userresults += [[user.first_name, totalscore]]
    sorted_score = OrderedDict()
    for username, score in sorted(userresults, key=lambda x: x[1], reverse=True):
        sorted_score[username] = score
    return render(request, "LenteCup/huidigestand.html",
                  {'scores': sorted_score})


def watgoktderest(request):
    users = User.objects.all()
    currentusers=[]
    for user in users:
        totaalgekozen = len(GekozenSpelers.objects.filter(user=user.pk))
        if totaalgekozen > 0:
            currentusers.append(user)
    scores = GekozenSpelers.objects.all().select_related('speler', 'user')
    tourstarted = tournamentstarted()

    return render(request, "LenteCup/watgoktderest.html",
                  {'scores': scores, 'users': currentusers, 'tourstarted': tourstarted})

