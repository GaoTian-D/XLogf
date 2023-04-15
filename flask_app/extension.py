#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: extension.py
- date: 23/10/2022
"""
from flask import session
from functools import wraps
from flask_app.utils.func import current_timestamp_second
from flask.sessions import SessionInterface
from flask import jsonify
import typing as t
import jwt


# https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         print(session)
#         if 'username' not in session:
#             return jsonify(code="301", message='会话失效, 即将跳转登录页面', data={})
#         return f(*args, **kwargs)
#
#     return decorated_function

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if 'username' not in session:
        #
        # # if not session.get("name"):
        # #     # if not there in the session then redirect to the login page
        # #     return redirect("/login")
        # ua = request.headers.get('User-Agent')
        # if ua and re.match(r'^audit-[\d\.]+\([\S ]+\)$', ua.strip()):
        #     return f(*args, **kwargs)
        # else:
            return jsonify(code="403", message='Forbidden', data={})

    return decorated_function

class JwtSession(dict):
    """Expands a basic dictionary with session attributes."""

    @property
    def permanent(self) -> bool:
        return True

    @permanent.setter
    def permanent(self, value: bool) -> None:
        pass

    #: Some implementations can detect changes to the session and set
    #: this when that happens. The mixin default is hard coded to
    #: ``True``.
    modified = True


class JwtCookieSessionInterface(SessionInterface):
    secret = "eaOh!Dva.9JV7qs"
    algorithm = "HS256"
    built_in_expire = '_expires'

    def encoded(self, session: dict):
        return jwt.encode(session, self.secret, algorithm=self.algorithm)

    def decode(self, jwtStr) -> dict:
        return jwt.decode(jwtStr, self.secret, algorithms=[self.algorithm])

    def open_session(
            self, app: "Flask", request: "Request"
    ) -> t.Optional[JwtSession]:
        val = request.cookies.get(self.get_cookie_name(app))
        if not val:
            return JwtSession({})
        try:
            expires = self.decode(val).get(self.built_in_expire)
            if expires and int(expires) > current_timestamp_second():
                # print(expires, current_timestamp_second())
                return JwtSession(self.decode(val))
        except Exception as e:
            print(e)
        return JwtSession({})

    def save_session(
            self, app: "Flask", session: JwtSession, response: "Response"
    ) -> None:
        name = self.get_cookie_name(app)
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        httponly = self.get_cookie_httponly(app)

        # If the session is modified to be empty, remove the cookie.
        # If the session is empty, return without setting the cookie.

        if not session:
            if session.modified:
                response.delete_cookie(
                    name,
                    domain=domain,
                    path=path,
                    secure=secure,
                    samesite=samesite,
                    httponly=httponly,
                )
            return

        if not self.should_set_cookie(app, session):
            return

        expires = self.get_expiration_time(app, session)
        session[self.built_in_expire] = expires
        response.set_cookie(
            name,
            self.encoded(session),
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite,
        )

    def get_expiration_time(
            self, app: "Flask", session: JwtSession
    ) -> t.Optional[int]:
        """A helper method that returns an expiration date for the session
        or ``None`` if the session is linked to the browser session.  The
        default implementation returns now + the permanent session
        lifetime configured on the application.
        """
        return current_timestamp_second() + app.permanent_session_lifetime.total_seconds()
