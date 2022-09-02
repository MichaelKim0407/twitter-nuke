import os

import requests
from requests_oauthlib import OAuth1

API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
USER_ID = os.environ['USER_ID']

auth = OAuth1(
    client_key=API_KEY,
    client_secret=API_KEY_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET,
)

session = requests.Session()
session.auth = auth
