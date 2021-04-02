from django.urls import path

from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path("change_password", views.change_password, name="change_password"),
]

