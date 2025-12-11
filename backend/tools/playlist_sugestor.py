from .spotify_base import get_spotify_token
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json
import requests
import random

def generate_consult(user_query: str) -> dict:
    
    llm = ChatOpenAI(response_format={"type": "json_object"}, model="gpt-4o-mini")
    prompt = """
        Você é um gerador de consultas otimizadas para buscas de playlists na API do Spotify.

        Sua tarefa é extrair palavras-chave relevantes da solicitação do usuário para encontrar a playlist ideal.

        REGRAS OBRIGATÓRIAS:
        - Extraia de 2 a 5 palavras-chave que descrevam o tema, mood, gênero ou contexto da playlist
        - Remova todos os acentos e caracteres especiais
        - Converta tudo para minúsculas
        - Separe as palavras com '+' (sem espaços)
        - NÃO inclua: "musica", "musicas", "playlist", verbos ("quero", "crie", "faça"), artigos ("uma", "para")
        - SE houver menção a país/nacionalidade, SEMPRE inclua nas keywords
        - SE houver menção a emoção/mood, SEMPRE inclua nas keywords
        - Priorize: gênero musical, emoção/mood, atividade, estilo, época, nacionalidade

        FORMATO DO RETORNO:
        Retorne APENAS um JSON válido:
        {
            "keywords": "palavra1+palavra2+palavra3"
        }

        EXEMPLOS:

        Usuário: "quero uma playlist de musicas tristes brasileiras"
        Saída: {"keywords": "tristes+brasileiras"}

        Usuário: "quero uma playlist para aniversario infantil"
        Saída: {"keywords": "aniversario+infantil+criancas"}

        Usuário: "quero uma playlist para treinar na academia"
        Saída: {"keywords": "treino+academia+motivacao"}

        Usuário: "playlist de rock dos anos 80"
        Saída: {"keywords": "rock+anos+80"}

        Usuário: "músicas calmas para estudar"
        Saída: {"keywords": "calmas+estudar+foco"}

        Usuário: "sertanejo romântico"
        Saída: {"keywords": "sertanejo+romantico"}
    """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )

    print(response.content)
    return json.loads(response.content)

def get_playlist_href(user_query: str) ->str:

    """Essa função é responsável por pegar o link de uma playlist existente"""

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

def get_playlist_id(user_query: str) -> str:

    """Essa função pega o id de uma playlist"""

    playlist_href = get_playlist_href(user_query)
    token = get_spotify_token()

    request = requests.get(
        playlist_href,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    id = request["playlists"]["items"][0]["id"]
    return id


@tool
def get_playlist_items(user_query):

    """
    Use esta ferramenta para sugestões de músicas baseadas em TEMA, MOOD, GÊNERO ou CONTEXTO (não artistas específicos).

    Exemplos de quando usar:
    - "crie uma playlist de [tema/mood/gênero]"
    - "sugira músicas [tema/mood/gênero]"
    - "quero uma playlist para [atividade/ocasião]"
    - "recomende músicas [tema/mood/gênero]"
    - "playlist de [gênero] [características]"
    - "músicas tristes brasileiras"
    - "playlist para treinar"
    - "músicas para estudar"

    Args:
        user_query: A consulta completa do usuário descrevendo o tipo de playlist desejada

    Returns:
        JSON com lista de músicas contendo: nome, link do Spotify, artista e popularidade
        Retorna até 50 músicas selecionadas aleatoriamente da playlist encontrada

    IMPORTANTE - QUANDO NÃO USAR:
    - NÃO use esta ferramenta para informações sobre artistas específicos
    - Para artistas específicos, use: get_artist_info, get_artist_albuns e get_artist_top_tracks
    - Use APENAS quando o foco for tema/mood/gênero/contexto SEM mencionar artista específico
    - Apresente as músicas de forma organizada com nome, artista e link clicável
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
        
        if len(musics) > 50:
            musics = random.sample(musics, 50)
    return musics
