import requests
from decouple import config


class OmdbError(Exception):
    """Raised when OMDB can't give us a usable movie (with a human message)."""


def fetch_movie_from_omdb(title):
    """
    Ask OMDB for one movie by title and translate its answer into OUR field
    names. Returns a dict shaped for MovieSerializer (+ a 'genres' name list).
    Raises OmdbError with a clear message when anything goes wrong.
    """
    try:
        response = requests.get(
            'https://www.omdbapi.com/',
            params={'t': title, 'apikey': config('OMDB_API_KEY')},  # -> ?t=...&apikey=...
            timeout=5,  # never call an external API without a timeout
        )
    except requests.RequestException:
        # DNS failure, timeout, connection refused... — anything network-level
        raise OmdbError('Could not reach OMDB. Check your internet or try again later.')

    data = response.json()

    # OMDB quirk: "movie not found" still comes back as HTTP 200 —
    # the real signal is a "Response": "False" field in the body.
    if data.get('Response') == 'False':
        raise OmdbError(f'OMDB has no movie titled "{title}".')

    # ---- Field mapping: OMDB dialect -> our model's language ----
    # OMDB uses the string "N/A" for missing values, so every field
    # goes through a cleanup before we trust it.

    def value_or_none(key):
        value = data.get(key)
        return None if value in (None, 'N/A', '') else value

    runtime = value_or_none('Runtime')                # "169 min" or None
    genre_string = value_or_none('Genre') or ''       # "Adventure, Drama, Sci-Fi"

    return {
        'title': data['Title'],
        'year': int(data['Year'][:4]),                # "2014" (or "2014–2016" for series)
        'director': value_or_none('Director') or 'Unknown',
        'plot': value_or_none('Plot') or '',
        'poster_url': value_or_none('Poster') or '',
        'imdb_rating': value_or_none('imdbRating'),   # string like "8.7" — DecimalField accepts it
        'runtime_minutes': int(runtime.split()[0]) if runtime else None,
        'language': value_or_none('Language') or '',
        'country': value_or_none('Country') or '',
        # genre NAMES — the view turns these into Category rows/ids
        'genres': [g.strip() for g in genre_string.split(',') if g.strip()],
    }
