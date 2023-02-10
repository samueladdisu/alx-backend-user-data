#!/usr/bin/env python3
"""
session_authentication views
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_session() -> str:
    """ post /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            ssid = auth.create_session(user.id)
            resp = make_response(user.to_json())
            resp.set_cookie(key=getenv("SESSION_NAME"), value=ssid)
            return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout_session() -> str:
    """ logout /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    res = auth.destroy_session(request)
    if not res:
        abort(404)
    return jsonify({})
