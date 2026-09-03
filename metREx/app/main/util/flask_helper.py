import hmac

from functools import wraps

from flask import abort, current_app, make_response, request


def get_request_api_key():
    api_key = request.headers.get('X-API-Key')
    if api_key is None:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.lower().startswith('bearer '):
            api_key = auth_header[7:].strip()
    return api_key


def require_api_key(func):
    """Rejects the request unless it carries the configured SCHEDULER_API_KEY."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected = current_app.config.get('SCHEDULER_API_KEY')
        if not expected:
            abort(503, 'Scheduler API is disabled: SCHEDULER_API_KEY is not configured.')
        provided = get_request_api_key()
        if provided is None or not hmac.compare_digest(str(provided), str(expected)):
            abort(401, 'A valid API key is required.')
        return func(*args, **kwargs)
    return wrapper


def format_response(data, content_type):
    response = make_response(data)

    response.headers['Content-Type'] = content_type
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
