from django.shortcuts import render, redirect

from LenteCup2.forms import ChangeFirstNameForm, ScoresForm
from LenteCup2.models import Week, Scores
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
