import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from spotipy import Spotify, SpotifyOAuth

from django.contrib.auth import login
from django.contrib.auth.models import User

import env
from . import models


def get_spotify_oauth():
    return SpotifyOAuth(
        scope=env.SPOTIFY_SCOPE,
        client_id=env.SPOTIFY_CLIENT_ID,
        client_secret=env.SPOTIFY_CLIENT_SECRET,
        redirect_uri=env.SPOTIFY_CALLBACK_URI,
        cache_handler=None, 
    )


def index(request):
    if "spotify_token" in request.session:
        return redirect(reverse("home:index"))
    return redirect(reverse("spotify:signin"))


def signin(request):
    auth_url = get_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


def callback(request):
    code = request.GET.get("code")
    if code:
        try:
            sp_oauth = get_spotify_oauth()
            token_info = sp_oauth.get_access_token(code, check_cache=False)
            request.session["spotify_token"] = token_info["access_token"]
        except Exception as e:
            messages.error(request, f"sp_oauth.get_access_token failed with: {str(e)}")
    else:
        messages.error(request, "No authorization code received from Spotify")

    print(token_info)
    continue_with_spotify(request, token_info)

    return redirect(reverse("home:events"))


def continue_with_spotify(request, token_info):
    sp = Spotify(auth=token_info['access_token'])
    profile = sp.current_user()
    spotify_id = profile['id']
    spotify_name = profile['display_name']

    if request.user.is_authenticated:
        # User is logged in, check if they have a Spotify account
        account = models.SpotifyAccount.objects.filter(user_id=request.user.id).first()
        if account:
            # Update existing account tokens
            account.access_token = token_info['access_token']
            account.refresh_token = token_info['refresh_token']
            account.expires_in = token_info['expires_in']
            account.expires_at = token_info['expires_at']
            account.last_synced = int(time.time())
            account.token_type = token_info['token_type']
            account.scope = token_info['scope']
            account.save()
        else:
            # Create new Spotify account for the user
            account = models.SpotifyAccount(
                user_id=request.user,
                account_id=spotify_id,
                expires_in=token_info['expires_in'],
                expires_at=token_info['expires_at'],
                last_synced=int(time.time()),
                access_token=token_info['access_token'],
                refresh_token=token_info['refresh_token'],
                token_type=token_info['token_type'],
                scope=token_info['scope']
            )
            account.save()
    else:
        # User is not logged in
        # Check if a user exists with this Spotify account
        account = models.SpotifyAccount.objects.filter(account_id=spotify_id).first()
        if account:
            # Update existing account tokens
            account.access_token = token_info['access_token']
            account.refresh_token = token_info['refresh_token']
            account.expires_in = token_info['expires_in'] 
            account.expires_at = token_info['expires_at']
            account.last_synced = int(time.time())
            account.token_type = token_info['token_type']
            account.scope = token_info['scope']
            account.save()
            # Log in the existing user
            login(request, account.user_id)
        else:
            # Create new user and Spotify account
            username = f"spotify_{spotify_id}"
            firstname = f"{spotify_name}"
            email = profile.get('email', '')
            
            # Create User
            user = User.objects.create_user(
                username=username,
                first_name=firstname,
                email=email,
                # Set unusable password since they'll log in with Spotify
                password=None
            )
            user.set_unusable_password()
            user.save()

            # Create SpotifyAccount
            account = models.SpotifyAccount(
                user_id=user,
                account_id=spotify_id,
                expires_in=token_info['expires_in'],
                expires_at=token_info['expires_at'],
                last_synced=int(time.time()),
                access_token=token_info['access_token'],
                refresh_token=token_info['refresh_token'],
                token_type=token_info['token_type'],
                scope=token_info['scope']
            )
            account.save()

            # Log in the new user
            login(request, user)

