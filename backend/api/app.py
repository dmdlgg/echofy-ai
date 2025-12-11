from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agent import agent

app = FastAPI()

# Permitir CORS para o front-end local
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

class ChatRequest(BaseModel):
	message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
	# Chama o agente com a mensagem do usuário
	result = agent.invoke({"messages": [{"role": "user", "content": req.message}]})
	reply = result["messages"][-1].content if "messages" in result and result["messages"] else "(Sem resposta)"
	return {"reply": reply}
