from langchain.tools import tool
from langchain_openai import ChatOpenAI
from .spotify_base import get_spotify_token
import requests


def generate_keywords(description: str) -> str:

    llm = ChatOpenAI(model="gpt-5-nano")
    prompt = f"""
    Transforme a descrição abaixo em palavras-chave para buscas no Spotify.
    Inclua APENAS de 3 a 6 palavras. Sem frases completas.

    Descrição: {description}
    """
    response = llm.invoke(
        [
            {"role": "user", "content": prompt}
        ]
    )
    return response.content

@tool
def create_playlist(description: str):

    """ Essa função  recebe uma descrição do usuario e faz uma busca, retornando musicas que batem com a descrição. 
        Devolva para o usuário o nome das musicas retornadas e o link para acessar cada uma.
        O input deve ser passado como parâmetro. 
    """
    keywords = generate_keywords(description)
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/search?q={keywords}&type=track&limit=10"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    )

    response = request.json()
    tracks = response.get("tracks", {}).get("items", [])

    return tracks

