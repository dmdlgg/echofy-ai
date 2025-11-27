from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from .tools.playlist_sugestor import get_playlist_items


# prompt para o agente
system_prompt = f"""
    Você é um agente útil que deve:

    1. Chamar a ferramenta necessaria UMA ÚNICA VEZ.
    2. Após a ferramenta retornar o JSON, você deve ANALISAR o JSON EXATAMENTE como ele veio.
    3. Você NÃO PODE inventar, corrigir, inferir ou alterar dados.
    4. Se o JSON vier vazio, você deve apenas informar que não houve resultados.
    5. Retorne ao usuário uma lista intuitiva do conteúdo do JSON.
    6. NUNCA chame a ferramenta novamente após receber o JSON.
    7. NUNCA modifique o JSON. Apenas LEIA e EXTRAIA.
    8. Retorne todo o conteúdo do JSON.
    9. Oriente o usuário e explique como funciona a reposta devolvida.

    Seja simpático e educado com os usuários e recuse educadamente pedidos fora do seu escopo.
    Retorne a resposta em formato markdown.
    Devolva a mensagem personalizada de forma adequada para o usuario.

"""

model = ChatOpenAI(model="gpt-4o-mini") 
agent = create_agent(model=model, system_prompt=system_prompt, tools=[get_playlist_items])

