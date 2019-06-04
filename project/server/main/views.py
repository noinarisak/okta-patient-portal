# project/server/main/views.py

import os
import json
import uuid

from flask import render_template, Blueprint, request
from flask import session, make_response, redirect

from project.server.utils.okta import OktaAuth

# main_blueprint = Blueprint("main", __name__)
main_blueprint = Blueprint("main", __name__)

# @main_blueprint.route("/")
# def home():
#     return render_template("main/home.html")


# @main_blueprint.route("/about/")
# def about():
#     return render_template("main/about.html")


# TODO: Move implementation to config.py
site_config = {
    "skin": os.getenv("SITE_SKIN", "blue"),
    "base_title": os.getenv("SITE_BASE_TITLE", "Medical Group"),
    "current_title": "",
    "app_title": os.getenv("SITE_APP_TITLE", "Patient Portal"),
    "app_logo": os.getenv("SITE_APP_LOGO", "images/logo_{0}.png".format(os.getenv("SITE_SKIN", "blue"))),
    "app_favicon": os.getenv("SITE_APP_FAVICON", "images/favicon.ico"),
    "app_slogan": os.getenv("SITE_APP_SLOGAN", "Get Better Sooner"),
}

okta_config = {
    "org_url": os.getenv("OKTA_ORG_URL", "<My Okta Org Here>"),
    "client_id": os.getenv("OKTA_CLIENT_ID", "<Client Id in Okta App>"),
    "client_secret": os.getenv("OKTA_CLIENT_SECRET", "<Client Secret in Okta App>"),
    "redirect_uri": os.getenv("OKTA_OIDC_REDIRECT_URI", "<OIDC Auth Code Endpoint for your app>"),
    "app_base_url": os.getenv("APP_BASE_URL", "<Default Landing URL for your app>"),
    "auth_server_id": os.getenv("OKTA_AUTH_SERVER_ID", None)
}

@main_blueprint.route("/")
@main_blueprint.route("/index")
def home():
    site_config["current_title"] = "{0} | {1} Home".format(site_config["base_title"],
                                                           site_config["app_title"])
    return render_template("index.html", site_config=site_config)


@main_blueprint.route('/oidc', methods=["POST"])
def oidc():
    """ handler for the oidc call back of the app """
    print("oidc()")
    #  print(request.form)

    if "error" in request.form:
        print("ERROR: {0}, MESSAGE: {1}".format(request.form["error"], request.form["error_description"]))

    if session["state"] == request.form["state"]:
        oidc_code = request.form["code"]
        #  print("oidc_code: {0}".format(oidc_code))
        okta_auth = OktaAuth(okta_config)
        oauth_token = okta_auth.get_oauth_token(
            code=oidc_code,
            grant_type="authorization_code",
            auth_options={
                "client_id": okta_config["client_id"],
                "client_secret": okta_config["client_secret"],
            }
        )
        #  print("oauth_token: {0}".format(json.dumps(oauth_token, indent=4, sort_keys=True)))
        app_landing_page_url = okta_config["app_base_url"]
        response = make_response(redirect(app_landing_page_url))
        response.set_cookie('token', oauth_token["access_token"])
        response.set_cookie('id_token', oauth_token["id_token"])
    else:
        print("FAILED TO MATCH STATE!!!")
        response = make_response(redirect("/"))

    session.pop("state", None)

    return response


@main_blueprint.route('/login', methods=["POST"])
def login():
    """ Handle either full form post redirect or a json response with redirect url """
    print("login()")
    auth_response = { "success": False }
    login_form_data = request.get_json()
    okta_auth = OktaAuth(okta_config)

    #  print("login_form_data: {0}".format(json.dumps(login_form_data, indent=4, sort_keys=True)))
    authn_json_response = okta_auth.authenticate(
        username=login_form_data["username"],
        password=login_form_data["password"],
        headers=request.headers)

    #  print("authn_json_response: {0}".format(json.dumps(authn_json_response, indent=4, sort_keys=True)))

    if "sessionToken" in authn_json_response:
        session["state"] = str(uuid.uuid4())
        oauth_authorize_url = okta_auth.create_oauth_authorize_url(
            response_type="code",
            state=session["state"],
            auth_options={
                "response_mode": "form_post",
                "prompt": "none",
                "scope": "openid",
                "sessionToken": authn_json_response["sessionToken"],
            }
        )

        auth_response["redirectUrl"] = oauth_authorize_url
        auth_response["success"] = True

        #  return make_response(redirect(oauth_authorize_url))
    else:
        auth_response["errorMessage"] = "Login Unsuccessful: {0}".format(authn_json_response["errorSummary"])

    return json.dumps(auth_response)


@main_blueprint.route("/logout", methods=["GET"])
def logout():
    print("logout()")

    redirect_url = "{host}/login/signout?fromURI={redirect_path}".format(
        host=okta_config["org_url"],
        redirect_path=okta_config["app_base_url"]
    )

    print("redirect_url: {0}".format(redirect_url))

    response = make_response(redirect(redirect_url))
    response.set_cookie("token", "")
    response.set_cookie("id_token", "")

    return response


@main_blueprint.route("/test")
def test():
    print("test()")

    if("token" in request.cookies):
        okta_auth = OktaAuth(okta_config)
        introspection_results_json = okta_auth.introspect(
            token=request.cookies.get("token"),
            headers=request.headers
        )
        print("introspection_results_json: {0}".format(json.dumps(introspection_results_json, indent=4, sort_keys=True)))

        if "active" in introspection_results_json:
            if introspection_results_json["active"]:
                print("Token is Valid")
            else:
                print("Token is Invalid")
        else:
            print("Token is Invalid")

    return "TEST"
