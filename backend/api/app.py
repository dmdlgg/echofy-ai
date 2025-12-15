import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.agent import agent

app = Flask(__name__)


allowed_origins = os.getenv('ALLOWED_ORIGINS').split(',')
CORS(app, origins=allowed_origins, supports_credentials=False)


conversation_history = []

@app.route("/chat", methods=["POST"])
def chat_endpoint():
	"""Endpoint principal para conversa com o agente"""
	global conversation_history
	
	data = request.get_json()
	message = data.get("message", "")
	
	
	conversation_history.append({"role": "user", "content": message})
	
	
	result = agent.invoke({"messages": conversation_history})
	reply = result["messages"][-1].content if "messages" in result and result["messages"] else "(Sem resposta)"
	
	
	conversation_history.append({"role": "assistant", "content": reply})
	
	return jsonify({"reply": reply})

@app.route("/chat/clear", methods=["DELETE"])
def clear_history():
	"""Endpoint para limpar o histórico de conversa"""
	global conversation_history
	conversation_history = []
	return jsonify({"message": "Histórico limpo com sucesso"})

@app.route("/health", methods=["GET"])
def health_check():
	"""Endpoint para health check do serviço"""
	return jsonify({"status": "healthy", "service": "echofy-ai"}), 200

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)
