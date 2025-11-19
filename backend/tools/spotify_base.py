import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_spotify_token():

    b64_str = os.getenv("B64_STR")

    headers = {
        "Authorization": f"Basic {b64_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )

    return response.json().get("access_token")

token = get_spotify_token()
print(token)