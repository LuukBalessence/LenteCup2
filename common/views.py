from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from common.forms import SignUpForm
from common.models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activeer je account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            recipient = [user]
            xx = send_mail(mail_subject, message, 'euro2020@balessence.nl', recipient, fail_silently=False, )
            print(xx)
            title = 'Bevestig a.u.b. je email'
            danger = 'info'
            notification1 = 'We hebben een activatie link naar je email adres gezonden!'
            notification2 = 'Controleer je email inbox (en spam folder) en klik op de link om je inschrijving te voltooien'
            return render(request, 'registration/email_confirm.html', {
                'notification1': notification1, 'notification2': notification2, 'title': title, 'info': danger
            })
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        title = 'We bevestigen hierbij je email'
        info = 'info'
        notification1 = 'Bedankt voor het bevestigen van je email.'
        notification2 = 'Je kunt nu inloggen. '
        return render(request, 'registration/email_confirm.html', {
            'notification1': notification1, 'notification2': notification2, 'title': title, 'info': info
        })
    else:
        title = 'We kregen je email niet bevestigd'
        danger = 'danger'
        notification1 = 'Activatie link is ongeldig!'
        notification2 = 'Bekijk a.u.b. je email. Heb je de hele activatie link gekopieerd?'
        return render(request, 'registration/email_confirm.html', {
            'notification1': notification1, 'notification2': notification2, 'title': title, 'info': danger
        })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Je wachtwoord is met succes bijgewerkt!')
            return redirect('change_password')
        else:
            messages.error(request, 'Corrigeer onderstaande fout.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
