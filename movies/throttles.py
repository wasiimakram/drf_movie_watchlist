from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# DRF's 3 built-in throttle classes (all in rest_framework.throttling):
#
# AnonRateThrottle   -> keys by IP address. Only throttles unauthenticated
#                       requests (get_cache_key returns None for logged-in
#                       users, so it silently skips them). What we use below
#                       since there's no JWT auth yet (Step 4).
#
# UserRateThrottle    -> keys by user ID instead of IP. Needs auth to exist
#                       first — add this ALONGSIDE AnonRateThrottle (not
#                       instead of it) once Step 4 is done, so logged-in
#                       users get their own (likely higher) limit and
#                       anonymous requests still get the stricter IP limit.
#
# ScopedRateThrottle  -> This provide ability to limit differently on every view means 
#                       every api, we can define limit separately.
#                       Just add `throttle_scope = 'name'` on a view and
#                       set that name's rate in
#                       REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']. e.g. POST
#                       could have a stricter limit than GET.


class MovieAnonThrottle(AnonRateThrottle):
    # Kept for reference — no longer wired into any view. Now that every
    # view requires IsAuthenticated, an anonymous request gets rejected by
    # the permission check before the throttle check ever runs (DRF checks
    # permissions before throttles), so this class would never trigger.
    rate = '5/min'


class MovieUserThrottle(UserRateThrottle):
    # Now that JWT auth is required on every view, this replaces
    # MovieAnonThrottle — keys by user ID instead of IP, higher limit
    # since a logged-in user is a known, trusted identity.
    rate = '50/min'
