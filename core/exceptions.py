from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Every exception (error) any view raises flows through here (wired in settings via
    EXCEPTION_HANDLER). We wrap DRF's normal error response in ONE consistent
    envelope so the frontend always gets the same shape:

        { "success": false, "status_code": 400, "errors": {...} }
    """
    # DRF's default handler builds the usual response (status + error data)
    # exception_handler only return API related error, if any app crash or something, it will return NONE
    response = exception_handler(exc, context)

    # response is None = not an API error but a real crash (a bug) —
    # We will simply bypass it, and not shape it, DRF own handler will catchup like yellow screen
    # But if its not None, then we will apply over shape on it.
    if response is not None:
        response.data = {
            'success': False,
            'status_code': response.status_code,
            'errors': response.data,
        }
    return response
