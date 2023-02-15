import os
import requests
from onedrive_auth_util import *

if (os.path.exists('refresh_token.txt')):
    refresh_token = load_refresh_token_from_file()
    access_token = get_new_access_token_using_refresh_token(refresh_token)
else:
    access_token = procure_new_tokens_from_user()
    save_access_token(str(access_token[0]))
    save_refresh_token(str(access_token[1]))
    access_token = access_token[0]

headers = {
    'Authorization': 'Bearer ' + access_token
}

response = requests.get(BASE_URL + 'me', headers=headers)

print(response.json())
