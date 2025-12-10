from .spotify_base import get_spotify_token
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import requests


def generate_artist_consult(user_query):
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = """
        Você é um gerador de consultas otimizadas para buscas de artistas na API do Spotify.

        Sua tarefa é extrair APENAS o nome do artista da solicitação do usuário e formatá-lo corretamente.

        REGRAS OBRIGATÓRIAS:
        - Extraia SOMENTE o nome do artista mencionado pelo usuário
        - Remova todos os acentos e caracteres especiais
        - Converta tudo para minúsculas
        - Separe palavras do nome do artista com '+' (sem espaços)
        - NÃO inclua: verbos ("quero", "me fale", "crie"), artigos ("o", "a", "os", "as"), ou palavras descritivas ("banda", "cantor", "informações")
        - Se houver múltiplos nomes ou sobrenomes, separe com '+'

        FORMATO DO RETORNO:
        Retorne APENAS o nome do artista formatado, nada mais.

        EXEMPLOS:

        Usuário: "quero informações sobre o john mayer"
        Saída: john+mayer

        Usuário: "me fale sobre a banda terno rei"
        Saída: terno+rei

        Usuário: "quero informações sobre a banda wallows"
        Saída: wallows

        Usuário: "álbuns do Arctic Monkeys"
        Saída: arctic+monkeys

        Usuário: "dados sobre a cantora Anitta"
        Saída: anitta
    """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )

    return response.content

def get_artist_id(query: str):

    artist = generate_artist_consult(query)
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    artist_data = request.get("artists").get("items")[0]
    id = artist_data.get("id")

    return id

@tool
def get_artist_info(user_query: str):

    """
    Use esta ferramenta quando o usuário solicitar informações, dados ou detalhes sobre um artista específico.

    Exemplos de quando usar:
    - "informações sobre [artista]"
    - "me fale sobre [artista]"
    - "quem é [artista]"
    - "dados do artista [artista]"
    - "gênero musical de [artista]"

    Args:
        user_query: A consulta completa do usuário contendo o nome do artista

    Returns:
        JSON completo com informações do artista: nome, gêneros, popularidade, seguidores, links e imagem

    IMPORTANTE: 
    - Chame esta ferramenta apenas UMA vez
    - Use o JSON retornado exatamente como vem, sem modificações
    - Não invente ou adicione informações que não estejam no JSON
    """
    
    artist = generate_artist_consult(user_query)
    token = get_spotify_token()

    search_url = (
        f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    artist_data = request.get("artists").get("items")[0]
    
    id = artist_data.get("id")
    name = artist_data.get("name")
    genres = artist_data.get("genres", [])
    popularity = artist_data.get("popularity")
    followers = artist_data.get("followers", {}).get("total")
    spotify_url = artist_data.get("external_urls", {}).get("spotify")
    
    images = artist_data.get("images", [])
    image_url = images[0].get("url") if images else None

    return {
        "id": id,
        "nome": name,
        "generos": genres,
        "popularidade": popularity,
        "seguidores": followers,
        "link_spotify": spotify_url,
        "imagem": image_url
    }


@tool
def get_artist_albuns(user_query):

    """
    Use esta ferramenta quando o usuário solicitar álbuns, discografia ou lançamentos de um artista específico.

    Exemplos de quando usar:
    - "álbuns do [artista]"
    - "discografia de [artista]"
    - "quais álbuns [artista] tem"
    - "mostre os álbuns de [artista]"
    - "lançamentos de [artista]"

    Args:
        user_query: A consulta completa do usuário contendo o nome do artista

    Returns:
        JSON com lista de nomes de álbuns do artista

    IMPORTANTE:
    - Chame esta ferramenta apenas UMA vez
    - Use o JSON retornado exatamente como vem, sem modificações
    - Não invente ou adicione informações que não estejam no JSON
    """


    token = get_spotify_token()
    id = get_artist_id(user_query)

    search_url = (
        f"https://api.spotify.com/v1/artists/{id}/albums"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    albuns = []
    items = request.get("items")
    for item in items:
        albuns.append(item.get("name"))

    return {"albuns": albuns}



