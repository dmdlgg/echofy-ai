# 🎵 Echofy AI

Um assistente inteligente especializado em música do Spotify, construído com LangChain e integração com a API do Spotify. O Echofy AI fornece informações detalhadas sobre artistas, álbuns, músicas e recomendações personalizadas baseadas em humor e preferências musicais.

## ✨ Funcionalidades

- 🎤 **Informações de Artistas**: Obtenha dados completos sobre artistas, incluindo gêneros, popularidade, seguidores e links do Spotify
- 💿 **Discografia Completa**: Explore álbuns de qualquer artista
- 🎶 **Top Músicas**: Descubra as músicas mais populares de cada artista
- 🎧 **Recomendações Personalizadas**: Receba sugestões de playlists baseadas em humor, gênero ou atividade
- 💬 **Interface de Chat Interativa**: Converse naturalmente com o assistente através de uma interface web moderna
- 
## 🏗️ Arquitetura

O projeto é dividido em duas partes principais:

### Backend (Python)
- **Framework**: Flask com Flask-CORS
- **IA/LLM**: LangChain + OpenAI (GPT)
- **Agente Inteligente**: LangGraph para orquestração de ferramentas
- **API**: Integração com Spotify Web API
- **Ferramentas especializadas**:
  - `data_analyst.py`: Análise de dados de artistas
  - `playlist_sugestor.py`: Sugestões de playlists
  - `spotify_base.py`: Autenticação e base para API do Spotify

### Frontend (TypeScript/Vite)
- **Framework**: Vite + TypeScript
- **Estilização**: Tailwind CSS
- **Renderização**: Marked.js para formatação de markdown
- **Interface**: Chat em tempo real com histórico de conversas

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Node.js 18+
- Conta no Spotify Developer
- Chave de API da OpenAI

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/echofy-ai.git
cd echofy-ai
```

### 2. Configuração do Backend

#### Instale as dependências Python

```bash
pip install -r requirements.txt
```

#### Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Spotify API
B64_STR=seu_codigo_base64_spotify

# OpenAI API
OPENAI_API_KEY=sua_chave_openai
```

**Como obter o B64_STR do Spotify:**

1. Acesse [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crie um aplicativo e obtenha `Client ID` e `Client Secret`
3. Encode em Base64: `echo -n "CLIENT_ID:CLIENT_SECRET" | base64`
4. Use o resultado no `.env`

#### Execute o servidor backend

```bash
python -m backend.api.app
```

O servidor estará disponível em `http://localhost:8000`

### 3. Configuração do Frontend

#### Instale as dependências Node

```bash
cd frontend
npm install
```

#### Execute o servidor de desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 📖 Uso

### Exemplos de Perguntas

**Informações de Artista:**
```
"Me fale sobre Coldplay"
"Quem é Taylor Swift?"
"Informações sobre The Beatles"
```

**Discografia:**
```
"Álbuns do Pink Floyd"
"Discografia do Queen"
"Quais álbuns do Radiohead?"
```

**Músicas Populares:**
```
"Músicas do Michael Jackson"
"Sucessos do Ed Sheeran"
"Top músicas do Metallica"
```

**Recomendações:**
```
"Músicas tristes para ouvir à noite"
"Playlist para treinar"
"Jazz relaxante"
"Músicas para estudar"
```

### API Endpoints

#### POST `/chat`
Envia uma mensagem para o assistente.

**Request:**
```json
{
  "message": "Me fale sobre Coldplay"
}
```

**Response:**
```json
{
  "reply": "Coldplay é uma banda britânica..."
}
```

#### DELETE `/chat/clear`
Limpa o histórico da conversa.

**Response:**
```json
{
  "message": "Histórico limpo com sucesso"
}
```

## 🛠️ Tecnologias Utilizadas

### Backend
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [LangChain](https://www.langchain.com/) - Framework para aplicações LLM
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Orquestração de agentes
- [OpenAI](https://openai.com/) - Modelo de linguagem
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - Dados musicais

### Frontend
- [Vite](https://vitejs.dev/) - Build tool
- [TypeScript](https://www.typescriptlang.org/) - Linguagem tipada
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS
- [Marked](https://marked.js.org/) - Parser de Markdown

## 📁 Estrutura do Projeto

```
echofy-ai/
├── backend/
│   ├── __init__.py
│   ├── agent.py              # Agente principal com LangChain
│   ├── api/
│   │   └── app.py           # API Flask
│   └── tools/               # Ferramentas do agente
│       ├── __init__.py
│       ├── data_analyst.py
│       ├── playlist_sugestor.py
│       └── spotify_base.py
├── frontend/
│   ├── api/
│   │   └── chatEndpoint.ts
│   ├── static/
│   │   ├── chat.ts
│   │   ├── index.html
│   │   └── style.css
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── requirements.txt
└── README.md
```

## 📬 Contato

Fique à vontade para entrar em contato caso tenha dúvidas, sugestões ou queira contribuir:
  
- 📨 **Email:** dumedolago@gmail.com 
- 💻 **Linkedin:** [Eduardo Medolago](https://www.linkedin.com/in/eduardo-medolago-364288259/)





⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
