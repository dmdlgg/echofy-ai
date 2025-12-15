// interface para a resposta do backend
interface ChatResponse {
  reply?: string;
}


const API_URL =  'http://localhost:8000';

// função para enviar mensagem ao backend
export async function sendToChatEndpoint(pergunta: string): Promise<string> {
  const resp = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: pergunta })
  });
  const data: ChatResponse = await resp.json();
  return data.reply || '(Sem resposta)';
}

export async function clearHistoryEndpoint(): Promise<void> {
  await fetch(`${API_URL}/chat/clear`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  });
}
