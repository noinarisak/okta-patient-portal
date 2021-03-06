import base64

from utils.rest import RestUtil


class OktaAuth:

    okta_config = None

    def __init__(self, okta_config):
        print("OktaAuth init()")
        if okta_config:
            self.okta_config = okta_config
        else:
            raise Exception("Requires okta_config")

    def authenticate(self, username, password, additional_options=None, headers=None):
        print("OktaAuth.authenticate()")
        url = "{host}/api/v1/authn".format(host=self.okta_config["org_url"])
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        body = {
            "username": username,
            "password": password,
        }

        if additional_options:
            RestUtil.map_attribute("audience", additional_options, body)
            RestUtil.map_attribute("relayState", additional_options, body)
            RestUtil.map_attribute("options", additional_options, body)
            RestUtil.map_attribute("context", additional_options, body)
            RestUtil.map_attribute("token", additional_options, body)

        return RestUtil.execute_post(url, body, okta_headers)

    def create_oauth_authorize_url(self, response_type, state, auth_options):
        print("OktaAuth.create_oauth_authorize_url()")

        url = (
            "{host}/oauth2{auth_server}/v1/authorize?"
            "response_type={response_type}&"
            "client_id={clint_id}&"
            "redirect_uri={redirect_uri}&"
            "state={state}"
        ).format(
            host=self.okta_config["org_url"],
            auth_server=OktaUtil.get_authserver_id(self.okta_config["auth_server_id"]),
            clint_id=self.okta_config["client_id"],
            redirect_uri=self.okta_config["redirect_uri"],
            state=state,
            response_type=response_type
        )

        if auth_options:
            for key in auth_options:
                url = "{url}&{key}={value}".format(url=url, key=key, value=auth_options[key])

        return url

    def get_oauth_token(self, code, grant_type, auth_options=None, headers=None):
        print("OktaAuth.get_oauth_token()")
        okta_headers = OktaUtil.get_oauth_okta_headers(headers)

        url = (
            "{host}/oauth2{auth_server}/v1/token?"
            "grant_type={grant_type}&"
            "code={code}&"
            "redirect_uri={redirect_uri}"
        ).format(
            host=self.okta_config["org_url"],
            auth_server=OktaUtil.get_authserver_id(self.okta_config["auth_server_id"]),
            code=code,
            redirect_uri=self.okta_config["redirect_uri"],
            grant_type=grant_type
        )

        body = {
            "authorization_code": code
        }

        if auth_options:
            for key in auth_options:
                url = "{url}&{key}={value}".format(url=url, key=key, value=auth_options[key])

        return RestUtil.execute_post(url, body, okta_headers)

    def introspect(self, token, headers=None):
        print("OktaAuth.introspect()")
        okta_headers = OktaUtil.get_oauth_okta_headers(headers, self.okta_config["client_id"], self.okta_config["client_secret"])

        url = "{host}/oauth2{auth_server}/v1/introspect?token={token}".format(
            host=self.okta_config["org_url"],
            auth_server=OktaUtil.get_authserver_id(self.okta_config["auth_server_id"]),
            token=token)
        body = {}

        return RestUtil.execute_post(url, body, okta_headers)


class OktaAdmin:
    def __init__(self, okta_config):
        print("OktaAdmin init()")


class OktaUtil:

    @staticmethod
    def get_default_okta_headers(headers):
        okta_default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        RestUtil.map_attribute("User-Agent", headers, okta_default_headers)
        RestUtil.map_attribute("X-Forwarded-For", headers, okta_default_headers)
        RestUtil.map_attribute("X-Forwarded-Port", headers, okta_default_headers)
        RestUtil.map_attribute("X-Forwarded-Proto", headers, okta_default_headers)

        return okta_default_headers

    @staticmethod
    def get_oauth_okta_headers(headers, client_id=None, client_secret=None):

        okta_oauth_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if client_id and client_secret:
            okta_oauth_headers["Authorization"] = "Basic {0}".format(OktaUtil.get_encoded_auth(client_id, client_secret))

        return okta_oauth_headers

    @staticmethod
    def get_encoded_auth(client_id, client_secret):
        print("get_encoded_auth()")
        auth_raw = "{client_id}:{client_secret}".format(
            client_id=client_id,
            client_secret=client_secret
        )

        encoded_auth = base64.b64encode(bytes(auth_raw, 'UTF-8')).decode("UTF-8")

        return encoded_auth

    @staticmethod
    def get_authserver_id(auth_server_id):
        auth_server = ""

        if auth_server_id:
            auth_server = "/{0}".format(auth_server_id)

        return auth_server
