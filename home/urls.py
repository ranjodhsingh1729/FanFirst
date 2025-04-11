from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("events/", views.events, name="events"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("events/<int:event_id>/buy-tickets/", views.buy_tickets, name="buy_tickets"),
]