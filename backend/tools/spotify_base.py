import requests
from dotenv import load_dotenv
import os


load_dotenv()

# essa função server para obter o bearer token para ter acesso a api do spotify
def get_spotify_token():

    b64_str = os.getenv("B64_STR") # codigo em base64 que é utilizado para gerar o token

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


