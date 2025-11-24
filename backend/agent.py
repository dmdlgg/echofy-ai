from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from .tools.playlist_creator import create_playlist
from dotenv import load_dotenv


# prompt para o agente
system_prompt = f"""
    Você é um agente que deve:

    1. Chamar a ferramenta necessaria UMA ÚNICA VEZ.
    2. Após a ferramenta retornar o JSON, você deve ANALISAR o JSON EXATAMENTE como ele veio.
    3. Você NÃO PODE inventar, corrigir, inferir ou alterar dados.
    4. Se o JSON vier vazio, você deve apenas informar que não houve resultados.
    5. Você deve extrair SOMENTE:
    6. Retorne ao usuário apenas uma lista limpa dos dados encontrados no JSON.
    7. NUNCA chame a ferramenta novamente após receber o JSON.
    8. NUNCA modifique o JSON. Apenas LEIA e EXTRAIA.
    9. Retorne TODAS as musicas encontradas no JSON.

"""

model = ChatOpenAI(model="gpt-4o-mini") 
agent = create_agent(model=model, system_prompt=system_prompt, tools=[create_playlist])
# result = agent.invoke({"messages": [{"role": "user", "content": "quero uma playlist de rock nacional dos anos 80"}]}) # teste de recomendações
# print(result["messages"][-1].content) # printa apenas a resposta do agente