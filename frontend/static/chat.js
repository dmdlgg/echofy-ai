import { sendToChatEndpoint } from '../api/chatEndpoint.js';

const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('input');

function addMsg(msg, role) {
  const div = document.createElement('div');
  div.className = 'mensagem ' + (role === 'user' ? 'usuario' : 'bot');
  div.textContent = (role === 'user' ? 'Você: ' : 'Bot: ') + msg;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const pergunta = input.value.trim();
  if (!pergunta) return;
  addMsg(pergunta, 'user');
  input.value = '';
  addMsg('...', 'bot');
  try {
    const resposta = await sendToChatEndpoint(pergunta);
    chat.lastChild.textContent = 'Bot: ' + resposta;
  } catch {
    chat.lastChild.textContent = 'Bot: Erro ao conectar ao backend.';
  }
};
