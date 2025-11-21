from langchain.tools import tool
from langchain_openai import ChatOpenAI
from .spotify_base import get_spotify_token
import requests
import json


# essa função foi criada com o proposito de transformar o pedido do usuario em palavras chaves para busca na api do spotify através de uma llm.
def generate_keywords(user_query: str) -> str:

    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"""
            Você é um gerador de palavras-chave otimizadas para buscas na API do Spotify.

            Sua tarefa é transformar a solicitação do usuário em uma frase curta composta por
            4 a 6 palavras-chave altamente relevantes, todas em minúsculas e separadas por '+'.

            REGRAS OBRIGATÓRIAS:
            - Não use preposições (de, para, com, por, em, etc.).
            - Não invente informações.
            - Use somente conceitos presentes na consulta.
            - Se a consulta mencionar um país ou nacionalidade, inclua isso nas palavras-chave.
            - Todas as palavras devem ser substantivos ou adjetivos úteis para busca (ex.: “tristes”, “brasileiras”, “eletronicas”).
            - Não adicionar verbos irrelevantes (ex.: “quero”, “ouvir”, “fazer”).
            - NÃO coloque nada além das palavras-chave.
            - Não use acentos.

            FORMATO DO RETORNO:
            palavra1+palavra2+palavra3+palavra4

            EXEMPLOS:

            Usuário: "quero uma playlist de musicas tristes brasileiras"
            Saída: musicas+tristes+lentas+brasileiras

            Usuário: "quero uma playlist para aniversario infantil"
            Saída: musicas+infantis+aniversario+brasileiras

            Usuário: "quero musicas para treinar na academia"
            Saída: musicas+academia+rapidas+energia+eletronicas

        """
    response = llm.invoke(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )
    print(response.content)
    return response.content

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
    keywords = generate_keywords(description)
    token = get_spotify_token() # obtem o token do spotify

    search_url = (
        f"https://api.spotify.com/v1/search?q={keywords}&type=track&limit=10"
    )

    request = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"}
    )

    response = request.json()

    tracks = response["tracks"]["items"]

    # captura apenas os dados essenciais para o agente analisar através de list compreheension
    processed = [ 
        {
            "name": t["name"],
            "artists": [a["name"] for a in t["artists"]],
            "url": t["external_urls"]["spotify"]
        }
        for t in tracks
    ]
    print(processed) # print para debug
    return processed

