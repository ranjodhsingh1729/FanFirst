import requests
from spotify.models import SpotifyAccount


def get_spotify_stats(request):
    is_connected = SpotifyAccount.objects.filter(user_id=request.user.id).first()
    if not is_connected:
        return {"connected": False}

    headers = {
        'Authorization': f'Bearer {is_connected.access_token}'
    }

    context = {"connected": True}

    # Fetch user's top artists
    top_artists = requests.get('https://api.spotify.com/v1/me/top/artists?limit=20&time_range=medium_term', headers=headers)
    if top_artists.status_code == 200:
        context['top_artists'] = top_artists.json().get('items', [])
    context['top_artists_len'] = len(context.get('top_artists', []))

    # Fetch followed artists
    followed_artists = requests.get('https://api.spotify.com/v1/me/following?type=artist&limit=20', headers=headers)
    if followed_artists.status_code == 200:
        context['followed_artists'] = followed_artists.json().get('artists', {}).get('items', [])
    context['followed_artists_len'] = len(context.get('followed_artists', []))

    # Fetch user's top tracks
    top_tracks = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=20&time_range=short_term', headers=headers)
    if top_tracks.status_code == 200:
        context['top_tracks'] = top_tracks.json().get('items', [])
    context['top_tracks_len'] = len(context.get('top_tracks', []))

    # Fetch recently played tracks
    recent_tracks = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=20', headers=headers)
    if recent_tracks.status_code == 200:
        context['recent_tracks'] = recent_tracks.json().get('items', [])
    context['recent_tracks_len'] = len(context.get('recent_tracks_len', []))

    # Fetch user profile
    profile = requests.get('https://api.spotify.com/v1/me', headers=headers)
    if profile.status_code == 200:
        context['spotify_profile'] = profile.json()

    return context
