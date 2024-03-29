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
from .views import home, explain, about

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("common/", include("common.urls")),
    path("euro2020/", include("euro2020.urls")),
    path("wk2022/", include("wk2022.urls")),
    path("luukopen21/", include("luukopen21.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("explain", explain, name="explain"),
    path("about", about, name="about"),
    path("changefirstname", views.changefirstname, name="changefirstname"),
    path("myaccount", views.myaccount, name="myaccount"),
    path("standinvoer", views.standinvoer, name="standinvoer"),
    path("jouwuitslagen", views.jouwuitslagen, name="jouwuitslagen"),
    path("overallstandlc", views.overallstandlc, name="overallstandlc"),
    path("weekuitslagen", views.weekuitslagen, name="weekuitslagen"),
    path("kiesspelers", views.kiesspelers, name="kiesspelers"),
    path("spelerslijst", views.spelerslijst, name="spelerslijst"),
    path("jouwspelers", views.jouwspelers, name="jouwspelers"),
    path("huidigestand", views.huidigestand, name="huidigestand"),
    path("watgoktderest", views.watgoktderest, name="watgoktderest"),
    path("masters2021", views.masters2021, name="masters2021"),
    path("lentecup2021", views.lentecup2021, name="lentecup2021"),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), ] + urlpatterns
