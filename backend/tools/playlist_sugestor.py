from .spotify_base import get_spotify_token
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json
import requests
import random

def generate_consult(user_query):
    
    llm = ChatOpenAI(response_format={"type": "json_object"}, model="gpt-4o-mini")
    prompt = """
        Você é um gerador de consultdas otimizadas para buscas na API do Spotify.

        Sua tarefa é transformar a solicitação do usuário em uma frase curta composta por 3 a 6 palavras-chave altamente relevantes, todas em minúsculas e separadas por '+'.

        REGRAS OBRIGATÓRIAS:
        - Não invente informações.
        - Não inclua a palavra "musicas" ou "musica" no resultado final
        - Use conceitos presentes na consulta.
        - Se a consulta mencionar um país ou nacionalidade, inclua isso nas palavras-chave. 
        - Não adicionar verbos irrelevantes (ex.: "quero", "crie", "faça").
        - Não use acentos.

        FORMATO DO RETORNO:
        Retorne um JSON com os campos:
        {
            "keywords": "palavra1+palavra2+palavra+palavra4",
        }

        EXEMPLOS:

        Usuário: "quero uma playlist de musicas tristes brasileiras"
        Saída: {"keywords": "tristes+brasileiras"}

        Usuário: "quero uma playlist para aniversario infantil"
        Saída: {"keywords": "aniversario+infantil"}

        Usuário: "quero uma playlist para treinar na academia"
        Saída: {"keywords": "academia"}
    """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )

    print(response.content)
    return json.loads(response.content)

def get_playlist_href(user_query):

    consult = generate_consult(user_query)
    final_consult = consult.get("keywords")
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/search?q={final_consult}&type=playlist&limit=1"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    href_playlist = request["playlists"]["href"]
    return href_playlist

def get_playlist_id(href):

    playlist_href = get_playlist_href(href)
    token = get_spotify_token()

    request = requests.get(
        playlist_href,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    id = request["playlists"]["items"][0]["id"]
    print(id)
    return id


@tool
def get_playlist_items(user_query):

    """
    Esta ferramenta deve ser chamada para sugerir musicas para playlists

    Esta ferramenta retorna sugestões de musicas para a criação de uma playlist

    Ela recebe a descrição do usuário, consulta a API do Spotify
    e retorna um JSON contendo as músicas encontradas.

    O modelo NÃO deve tentar corrigir o JSON. 
    O valor retornado por esta ferramenta deve ser entregue diretamente ao agente,
    sem chamar novamente a ferramenta.
    """

    playlist_id = get_playlist_id(user_query)
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    )
    
    response = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    musics = []

    for item in response["items"]:
        music_link = item.get("track").get("external_urls").get("spotify")
        music_name = item.get("track").get("name")
        music_artist = item.get("track").get("artists")[0].get("name")
        music_popularity = item.get("track").get("popularity")
        musics.append(
            {
                "nome": music_name, 
                "link": music_link, 
                "artista": music_artist,
                "popularity": music_popularity
            }
        )
        
        #musics = sorted(musics, key=lambda x: x["popularity"], reverse=True)
        if len(musics) > 50:
            musics = random.sample(musics, 50)
    return musics
