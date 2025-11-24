// Função para enviar mensagem ao backend
export async function sendToChatEndpoint(pergunta) {
  const resp = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: pergunta })
  });
  const data = await resp.json();
  return data.reply || '(Sem resposta)';
}
