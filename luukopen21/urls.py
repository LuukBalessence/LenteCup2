"""LenteCup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("aanmelden", views.aanmelden, name="aanmelden"),
    path("scumofthegolfcourse", views.scumofthegolfcourse, name="scumofthegolfcourse"),
    path("praktischeinfo", views.praktischeinfo, name="praktischeinfo"),
    path("lijstaanmeldingen", views.lijstaanmeldingen, name="lijstaanmeldingen"),
    path("usermenu", views.usermenu, name="usermenu"),
    path("donderdag", views.donderdag, name="donderdag"),
    path("vrijdag", views.vrijdag, name="vrijdag"),
    path("zaterdag", views.zaterdag, name="zaterdag"),
    path("zondag", views.zondag, name="zondag"),
    path("preluukopen", views.preluukopen, name="preluukopen"),
    path("speldo1", views.speldo1, name="speldo1"),
    path("heather", views.heather, name="heather"),
    path("clubsblack", views.clubsblack, name="clubsblack"),
    path("blackmystery", views.blackmystery, name="blackmystery"),
    path("foursomes", views.foursomes, name="foursomes"),
    path("fourballs", views.fourballs, name="fourballs"),
    path("singles", views.singles, name="singles"),
    path("halvefinale", views.halvefinale, name="halvefinale"),
    path("finale", views.finale, name="finale"),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), ] + urlpatterns
