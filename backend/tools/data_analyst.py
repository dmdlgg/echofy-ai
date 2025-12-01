"""
inicio da construção da tool de info sobre artistas
passos:
1. get no endpoint search com o nome do artista:
        capturar o id do artista
        capturar os generos

2. get no endpoint de artist albuns:
        pegar o nome de cada album
        pegar o album mais famoso


"""

from spotify_base import get_spotify_token
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json
import requests
import random


def generate_artist_consult(user_query):
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = """
        Você é um gerador de consultdas otimizadas para buscas na API do Spotify.

        Sua tarefa é transformar a solicitação do sobre um artista em apenas o nome do artista, em minúsculas e separado por '+'.

        REGRAS OBRIGATÓRIAS:
        - Não invente informações.
        - Use somente informações presentes na consulta.
        - Não adicionar verbos irrelevantes (ex.: "quero", "crie", "faça").
        - Não use acentos.

        FORMATO DO RETORNO:
        Deve ser apenas o nome do artista mencionado, sem nada mais. 

        EXEMPLOS:

        Usuário: "quero informações sobre o john mayer"
        Saída: "john+mayer"

        Usuário: "me fale sobre a banda terno rei"
        Saída: "terno+rei"

        Usuário: "quero informções sobre a banda wallows"
        Saída: "wallows"
    """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )

    print(response.content)
    return response.content

def get_artist_info(user_query: str):
    
    artist = generate_artist_consult(user_query)
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    id =  request.get("artists").get("items")[0].get("id")
    genres = request.get("artists").get("items")[0].get("genres")

    print(search_url)
    print(genres, id)

get_artist_info("quero informações sobre o artista john mayer")
