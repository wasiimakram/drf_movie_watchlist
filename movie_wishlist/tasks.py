"""
ONE central place for every background task in the project, instead of a
tasks.py per app. Group by app with a comment header
"""
from celery import shared_task
from categories.models import Category
from movies.serializers import MovieSerializer
from movies.services import fetch_movie_from_omdb, OmdbError


# ---------------- movies ----------------
"""
@shared_task is the marker that makes a function queueable. 
Only functions decorated this way get the special powers
"""
@shared_task
def import_movie_task(title):
    """
    Runs in the Celery WORKER process, not the web request. Same logic as
    MovieImportAPIView.post() (concept #28), just triggered by .delay()
    instead of an HTTP request — one job per title, queued via Redis.
    """
    try:
        movie_data = fetch_movie_from_omdb(title)
    except OmdbError:
        # One bad title shouldn't stop the whole batch — just skip it.
        return f'Skipped "{title}": not found on OMDB.'

    category_ids = []
    for genre_name in movie_data.pop('genres'):
        category, _created = Category.objects.get_or_create(name=genre_name)
        category_ids.append(category.id)
    movie_data['category'] = category_ids

    serializer = MovieSerializer(data=movie_data)
    if serializer.is_valid():
        serializer.save()
        return f'Imported "{title}".'
    return f'Skipped "{title}": {serializer.errors}'
