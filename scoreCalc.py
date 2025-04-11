import requests
from spotify.models import SpotifyAccount
from spotifystats import get_spotify_stats

def calc_score(request, artist_name):
    try:
        context = get_spotify_stats(request)
        print(context)
        score = 0
        top_artists = context.get('top_artists', [])
        top_artists = [artist.get('name') for artist in top_artists]
        print(top_artists)
        if artist_name in top_artists:
            score += int(2.5*top_artists.index(artist_name))
        followed_artists = context.get('followed_artists', [])
        followed_artists = [artist.get('name') for artist in followed_artists]
        print(followed_artists)
        if artist_name in followed_artists:
            score += 10
        return score
    except Exception as e:
        print(e)
        return -1
