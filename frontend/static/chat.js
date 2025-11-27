import { sendToChatEndpoint } from '../api/chatEndpoint.js';


const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('input');

document.documentElement.classList.add('dark');
localStorage.setItem('theme', 'dark');


function addMsg(msg, role) {
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

function addTypingIndicator() {
  const wrapper = document.createElement('div');
  wrapper.className = 'bot typing-wrapper';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = '🤖';

  const typingDiv = document.createElement('div');
  typingDiv.className = 'typing-indicator';
  typingDiv.innerHTML = '<span></span><span></span><span></span>';

  wrapper.appendChild(avatar);
  wrapper.appendChild(typingDiv);
  chat.appendChild(wrapper);
  chat.scrollTop = chat.scrollHeight;
  return wrapper;
}

function removeTypingIndicator(typingWrapper) {
  if (typingWrapper && typingWrapper.parentNode) {
    typingWrapper.parentNode.removeChild(typingWrapper);
  }
}

form.onsubmit = async (e) => {
  e.preventDefault();
  const pergunta = input.value.trim();
  if (!pergunta) return;
  addMsg(pergunta, 'user');
  input.value = '';
 
  await new Promise(resolve => setTimeout(resolve, 1500));
  const typingWrapper = addTypingIndicator();
  try {
    const resposta = await sendToChatEndpoint(pergunta);
    removeTypingIndicator(typingWrapper);
    addMsg(resposta, 'bot');
  } catch {
    removeTypingIndicator(typingWrapper);
    addMsg('Erro ao conectar ao backend.', 'bot');
  }
};
