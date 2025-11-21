# 🎵 Echofy – Assistente para o Spotify com IA (em desenvolvimento)

Este projeto utiliza **IA generativa** para interpretar descrições em linguagem natural e convertê-las em buscas otimizadas na **API do Spotify**.  
A ferramenta entende intenções musicais — emoção, energia, contexto e até nacionalidade associada a gêneros — e retorna uma lista de músicas relevantes, podendo criar playlists e fazer análise de dados.

⚠️Aviso: Este projeto ainda está em desenvolvimento e novas funcionalidades serão adicionadas futuramente.

---

## 🚀 Funcionalidades

A primeira funcionalidade (que ainda está em desenvolvimento) é solicitar músicas de um certo estilo ou gênero, e o agente vai usar a API do Spotify para criar uma playlist com músicas que se encaixem com o que foi solicitado.

## 🧠 Como funciona

1. O usuário envia uma descrição em texto.  
2. Uma função utiliza uma LLM para transformar essa descrição em palavras-chave
3. Essas palavras são usadas para fazer uma busca na API, retornando um JSON
4. O agente analisa e cria uma playlist com as musicas retornadas.

---

## 🛠️ Tecnologias

- **Python**
- **LangChain**
- **OpenAI GPT-4o-mini**
- **Spotify Web API**
- **Postman** (para testes com a API)
- **FastAPI** (para a criação da API que vai se comunicar com o front-end)
- **React** (para a criação da interface)

---
## 📬 Contato

Fique à vontade para entrar em contato caso tenha dúvidas, sugestões ou queira contribuir:
  
- 📨 **Email:** dumedolago@gmail.com 
- 💻 **Linkedin:** [Eduardo Medolago](https://www.linkedin.com/in/eduardo-medolago-364288259/)
