import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    """
    A FilterSet is just a translator: it reads query params from the URL
    and turns them into Django ORM lookups (the same .filter(field__lookup=value)
    calls you'd write by hand in the shell).

    Every attribute below is a separate declared filter -> one query param.
    """

    # --- Category (Many-to-Many) ---
    # 'category__id' walks THROUGH the M2M join table, same as the
    # double-underscore relation traversal you use in querysets/ORM lookups.
    # ?category=2  ->  Movie.objects.filter(category__id=2)
    category = django_filters.NumberFilter(field_name='category__id')

    # --- Director (partial text match) ---
    # icontains = case-insensitive "contains" -> ?director=nolan matches
    # "Christopher Nolan" too, not just an exact full-string match.
    director = django_filters.CharFilter(field_name='director', lookup_expr='icontains')


    # --- Year range ---
    # ?year_min=2000  ->  Movie.objects.filter(year__gte=2000)
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    # ?year_max=2015  ->  Movie.objects.filter(year__lte=2015)
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')

    # --- IMDB rating range ---
    # Two filters pointed at the SAME model field (imdb_rating), just with
    # different lookup_expr ('gte' vs 'lte') and different query param names.
    # ?rating_min=7.5  ->  Movie.objects.filter(imdb_rating__gte=7.5)
    rating_min = django_filters.NumberFilter(field_name='imdb_rating', lookup_expr='gte')
    # ?rating_max=9    ->  Movie.objects.filter(imdb_rating__lte=9)
    rating_max = django_filters.NumberFilter(field_name='imdb_rating', lookup_expr='lte')

    # --- Runtime range ---
    # ?runtime_min=90  ->  Movie.objects.filter(runtime_minutes__gte=90)
    runtime_min = django_filters.NumberFilter(field_name='runtime_minutes', lookup_expr='gte')
    # ?runtime_max=150 ->  Movie.objects.filter(runtime_minutes__lte=150)
    runtime_max = django_filters.NumberFilter(field_name='runtime_minutes', lookup_expr='lte')

    

    class Meta:
        model = Movie
        # 'language' and 'country' aren't declared above as attributes, so
        # listing them here makes django-filter auto-generate simple EXACT
        # match filters for them -> ?language=English, ?country=USA
        fields = [
            'year_min', 'year_max',
            'rating_min', 'rating_max',
            'runtime_min', 'runtime_max',
            'category', 'director',
            'language', 'country',
        ]
