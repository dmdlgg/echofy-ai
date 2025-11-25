import { sendToChatEndpoint } from '../api/chatEndpoint.js';


const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('input');

document.documentElement.classList.add('dark');
localStorage.setItem('theme', 'dark');


function addMsg(msg, role) {
  // Estrutura com avatar
  const wrapper = document.createElement('div');
  wrapper.className = role === 'user' ? 'usuario' : 'bot';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? '🧑' : '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'mensagem';

  if (role === 'bot' && window.marked) {
    bubble.innerHTML = window.marked.parse(msg);
  } else {
    bubble.textContent = msg;
  }

  if (role === 'user') {
    wrapper.appendChild(bubble);
    wrapper.appendChild(avatar);
  } else {
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
  }
  chat.appendChild(wrapper);
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
    // Substitui a última mensagem do bot pelo markdown renderizado
    const lastBot = chat.querySelector('.bot:last-child .mensagem');
    if (lastBot && window.marked) {
      lastBot.innerHTML = window.marked.parse(resposta);
    } else if (lastBot) {
      lastBot.textContent = resposta;
    }
  } catch {
    const lastBot = chat.querySelector('.bot:last-child .mensagem');
    if (lastBot) lastBot.textContent = 'Erro ao conectar ao backend.';
  }
};
