from flask import abort
from flask_login import current_user
from functools import wraps

def requiere_rol(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper
