// interface para a resposta do backend
interface ChatResponse {
  reply?: string;
}

// função para enviar mensagem ao backend
export async function sendToChatEndpoint(pergunta: string): Promise<string> {
  const resp = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: pergunta })
  });
  const data: ChatResponse = await resp.json();
  return data.reply || '(Sem resposta)';
}
