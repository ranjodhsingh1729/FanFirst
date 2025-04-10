from django.shortcuts import render, redirect
from django.http import HttpResponse
from spotipy import SpotifyOAuth
from django.urls import reverse

# :)
import env


# Configure Spotify OAuth
sp_oauth = SpotifyOAuth(
    scope=env.SPOTIFY_SCOPE,
    client_id=env.SPOTIFY_CLIENT_ID,
    client_secret=env.SPOTIFY_CLIENT_SECRET,
    redirect_uri=env.SPOTIFY_CALLBACK_URI,
)


def index(request):
    if "spotify_token" in request.session:
        return redirect(reverse("home"))
    return redirect(reverse("spotify.signin"))


def signin(request):
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def callback(request):
    code = request.GET.get("code", None)
    if code is not None:
        access_token = sp_oauth.get_access_token(code)
        request.session["spotify_token"] = access_token["access_token"]
    else:
        pass

    return redirect(reverse("home"))
