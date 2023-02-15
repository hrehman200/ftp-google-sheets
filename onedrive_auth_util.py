import msal
import webbrowser
import requests
import json
import os

APP_ID = 'xxx'
CLIENT_SECRET = 'xxx'
APP_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
SCOPES = ["Files.ReadWrite.All"]

AUTHORITY_URL = "https://login.microsoftonline.com/consumers/"
BASE_URL = "https://graph.microsoft.com/v1.0/"


def procure_new_tokens_from_user() -> tuple:
    endpoint = BASE_URL + "me"
    SCOPES = ["User.Read", "User.Export.All, Files.ReadWrite.All"]
    client_instance = msal.ConfidentialClientApplication(
        client_id=APP_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY_URL)
    authorization_request_url = client_instance.get_authorization_request_url(
        SCOPES)
    webbrowser.open(authorization_request_url)
    # print(authorization_request_url)
    print("")
    print("Please enter the code you see in the URL on the web browser:")
    authorization_code = input()
    # example: authorization_code = "M.R3_BAY.ec1e0d91-e035-0065-f757-494a9c206744"
    tokenDictionary = client_instance.acquire_token_by_authorization_code(
        code=authorization_code, scopes=SCOPES)
    # print(tokenDictionary)
    access_token = tokenDictionary["access_token"]
    refresh_token = tokenDictionary["refresh_token"]
    name = tokenDictionary["id_token_claims"]["name"]
    return (access_token, refresh_token, name)


def load_access_token_from_file() -> str:
    try:
        with open(APP_PATH + "access_token.txt") as f:
            line = f.readline()
        return line
    except:
        return None


def load_refresh_token_from_file() -> str:
    try:
        with open(APP_PATH + "refresh_token.txt") as f:
            line = f.readline()
        return line
    except:
        return None


def save_access_token(token: str):
    with open(APP_PATH + "access_token.txt", "w") as f:
        f.write(token)
    return


def save_refresh_token(token: str):
    with open(APP_PATH + "refresh_token.txt", "w") as f:
        f.write(token)
    return

# see https://learn.microsoft.com/en-us/graph/auth-v2-user?view=graph-rest-1.0#5-use-the-refresh-token-to-get-a-new-access-token


def get_new_access_token_using_refresh_token(refresh_token: str):

    request_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    scope_list = ["https://graph.microsoft.com/Files.ReadWrite.All"]
    scope = "%20".join(scope_list)
    redirect_uri = (
        f"http://localhost/"
    )

    payload = {
        "client_id": APP_ID,
        "client_secret": CLIENT_SECRET,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(url=request_url, headers=headers, data=payload)
    # print(response.content)
    responseText = response.text
    # print(responseText)
    j = json.loads(responseText)

    return j["access_token"]
