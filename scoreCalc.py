import requests
from spotify.models import SpotifyAccount
from spotifystats import get_spotify_stats

def calc_score(request, artist_name):
    try:
        context = get_spotify_stats(request)

        score = 0
        top_artists = context.get('top_artists', [])
        if artist_name in top_artists:
            score += int(2.5*top_artists.index(artist_name))
        followed_artists = context.get('followed_artists', [])
        if artist_name in followed_artists:
            score += 10
        return score
    except:
        return -1