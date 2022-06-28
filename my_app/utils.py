from flask import flash, redirect,url_for
from flask_login import current_user
from functools import wraps

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.group != 0:        # zero means admin, one and up are other groups
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("main.profile"))
        return func(*args, **kwargs)
    return decorated_view