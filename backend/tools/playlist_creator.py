from langchain.tools import tool
from langchain_openai import ChatOpenAI
from .spotify_base import get_spotify_token
import requests
import json


# essa função foi criada com o proposito de transformar o pedido do usuario em palavras chaves para busca na api do spotify através de uma llm.
def generate_keywords(user_query: str) -> dict:

    llm = ChatOpenAI(response_format={"type": "json_object"}, model="gpt-4o-mini")
    prompt = """
        Você é um gerador de palavras-chave otimizadas para buscas na API do Spotify.

        Sua tarefa é transformar a solicitação do usuário em uma frase curta composta por 4 a 6 palavras-chave altamente relevantes, todas em minúsculas e separadas por ' '.

        REGRAS OBRIGATÓRIAS:
        - Não usar preposições (of, for, with, by, in, etc.).
        - Não invente informações.
        - Use somente conceitos presentes na consulta.
        - Se a consulta mencionar um país ou nacionalidade, inclua isso nas palavras-chave.
        - Todas as palavras devem ser substantivos ou adjetivos úteis para busca (ex.: "sad", "brazilian", "electronic").
        - Pelo menos uma palavra deve ser o sentimento que o tipo de música pedida pelo usuário transmite (ex: "sad", "happy").
        - Não adicionar verbos irrelevantes (ex.: "want", "listen", "make").
        - Não use acentos.

        FORMATO DO RETORNO:
        Retorne um JSON com os campos:
        {
            "keywords": "palavra1 palavra2 palavra palavra4",
            "genre": "um genero musical valido do Spotify Web API relacionado à nacionalidade mencionada na consulta do usuario. Exemplo: se na consulta é mencionado a nacionalidade/pais brasileira/brasil, esse campo deve ser preenchido com um genero valido desse pais e que condiza com o tipo de musica procurado. Exemplo: musicas tristes indies brasileiras. Deve ser preenchido com: mpb."
        }

        EXEMPLOS:

        Usuário: "quero uma playlist de musicas tristes brasileiras"
        Saída: {"keywords": "sad slow brazilian", "genre": "mpb"}

        Usuário: "quero uma playlist para aniversario infantil"
        Saída: {"keywords": "kids birthday", "genre": "children"}

        Usuário: "quero musicas para treinar na academia"
        Saída: {"keywords": "gym fast energy electronic", "genre": "workout"}
    """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )
    print(response.content)
    return json.loads(response.content)

@tool
def create_playlist(description: str) -> dict:

    """
    Esta ferramenta deve ser chamada **apenas uma vez por solicitação do usuário**.
    O modelo NÃO deve chamar esta ferramenta mais de uma vez.

    Ela recebe a descrição do usuário, consulta a API do Spotify
    e retorna um JSON contendo as músicas encontradas.

    O modelo NÃO deve tentar corrigir o JSON. 
    O valor retornado por esta ferramenta deve ser entregue diretamente ao agente,
    sem chamar novamente a ferramenta.
    """
    print("tool chamada") # debug para saber se a tool está sendo chamada (remover depois)
    keywords_and_genre = generate_keywords(description)
    keywords = keywords_and_genre.get("keywords")
    genre = keywords_and_genre.get("genre")
    token = get_spotify_token() # obtem o token do spotify

    search_url = (
        f"https://api.spotify.com/v1/search?q={keywords}&type=track&limit=50&genre:{genre}"
    )
    print(search_url)

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    )

    response = request.json()

    tracks = response["tracks"]["items"]
    processed = [
        {
            "name": t["name"],
            "artists": [a["name"] for a in t["artists"]],
            "url": t["external_urls"]["spotify"],
            "popularity": t.get("popularity", 0)
        }
        for t in tracks
    ]
    return sorted(processed, key=lambda x: x["popularity"], reverse=True)[:10] #retorna a lista ordenada por popularidade, pegando as 10 mais famosas