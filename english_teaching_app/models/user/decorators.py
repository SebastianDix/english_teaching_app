#!/usr/bin/env python3
import functools
from typing import Callable

from flask import session, flash,redirect, url_for, current_app,request

def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in to view this page','danger')
            return redirect(url_for('users.login_user',next=request.url))
        return f(*args,**kwargs)
    return decorated_function

def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN',''):
            flash('But are you an admin though?','danger')
            return redirect(url_for('users.login_user',next=request.url))
        return f(*args,**kwargs)
    return decorated_function

