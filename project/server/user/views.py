# project/server/user/views.py

import os
import json
import uuid

from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask import Flask, session, send_from_directory, make_response
from flask_sslify import SSLify # TODO: look this shit up
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm
from project.server.utils.okta import OktaAuth


user_blueprint = Blueprint("user", __name__)

# # TODO: Move this to config.py
# okta_config = {
#     "org_url": os.getenv("OKTA_ORG_URL", "<My Okta Org Here>"),
#     "client_id": os.getenv("OKTA_CLIENT_ID", "<Client Id in Okta App>"),
#     "client_secret": os.getenv("OKTA_CLIENT_SECRET", "<Client Secret in Okta App>"),
#     "redirect_uri": os.getenv("OKTA_OIDC_REDIRECT_URI", "<OIDC Auth Code Endpoint for your app>"),
#     "app_base_url": os.getenv("APP_BASE_URL", "<Default Landing URL for your app>"),
#     "auth_server_id": os.getenv("OKTA_AUTH_SERVER_ID", None)
# }

# @user_blueprint.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         user = User(email=form.email.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()

#         login_user(user)

#         flash("Thank you for registering.", "success")
#         return redirect(url_for("user.members"))

#     return render_template("user/register.html", form=form)


# @user_blueprint.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(
#             user.password, request.form["password"]
#         ):
#             login_user(user)
#             flash("You are logged in. Welcome!", "success")
#             return redirect(url_for("user.members"))
#         else:
#             flash("Invalid email and/or password.", "danger")
#             return render_template("user/login.html", form=form)
#     return render_template("user/login.html", title="Please Login", form=form)

# @user_blueprint.route('/login', methods=["GET", "POST"])
# def login():
#     """ Handle either full form post redirect or a json response with redirect url """
#     print("login()")
#     auth_response = { "success": False }
#     login_form_data = request.get_json()
#     okta_auth = OktaAuth(okta_config)

#     #  print("login_form_data: {0}".format(json.dumps(login_form_data, indent=4, sort_keys=True)))
#     authn_json_response = okta_auth.authenticate(
#         username=login_form_data["username"],
#         password=login_form_data["password"],
#         headers=request.headers)

#     # print("authn_json_response: {0}".format(json.dumps(authn_json_response, indent=4, sort_keys=True)))

#     if "sessionToken" in authn_json_response:
#         session["state"] = str(uuid.uuid4())
#         oauth_authorize_url = okta_auth.create_oauth_authorize_url(
#             response_type="code",
#             state=session["state"],
#             auth_options={
#                 "response_mode": "form_post",
#                 "prompt": "none",
#                 "scope": "openid",
#                 "sessionToken": authn_json_response["sessionToken"],
#             }
#         )

#         auth_response["redirectUrl"] = oauth_authorize_url
#         auth_response["success"] = True

#         #  return make_response(redirect(oauth_authorize_url))
#     else:
#         auth_response["errorMessage"] = "Login Unsuccessful: {0}".format(authn_json_response["errorSummary"])

#     return json.dumps(auth_response)

# @user_blueprint.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("You were logged out. Bye!", "success")
#     return redirect(url_for("main.home"))


# @user_blueprint.route("/members")
# @login_required
# def members():
#     return render_template("user/members.html")
