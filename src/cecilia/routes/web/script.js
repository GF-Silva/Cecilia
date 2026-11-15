import { fetchEventSource } from 'https://esm.sh/@microsoft/fetch-event-source';

const messages = document.getElementById('messages');
const prompt = document.getElementById('prompt');
const uuidReg = /chats\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/
let chatId = window.location.pathname.match(uuidReg)?.[1];

if (chatId) {
    await buildContext(chatId);
}

prompt.addEventListener('keydown', (evt) => {
    if (evt.key != 'Enter' || evt.shiftKey || evt.isComposing) return;

    evt.preventDefault();

    const text = prompt.value.trim();

    if (!text) return;

    send_prompt(text);

    prompt.value = '';
})

async function buildContext(chatId) {
    const response = await fetch(`/v1/chats/${chatId}/messages`);

    if (!response.ok) {
        throw new Error('Falha iniciando context');
    }

    const data = await response.json();

    data.forEach(msg => {
        createMessage(msg['is_user'] ? 'user' : 'assistant', msg['text']);
    });
}

function createMessage(role, content) {
    const message = document.createElement('div');
    message.className = `message ${role == 'user' ? 'message__user' : 'message__assistant'}`;

    const text = document.createElement('p');
    text.innerHTML = content ? marked.parse(content) : null;

    message.append(text);

    messages.scrollTop = messages.scrollHeight;
    messages.append(message);

    return message;
}

function updateContent(message, text) {
    message.dataset.text = message.dataset.text ? message.dataset.text + text : text;
    message.innerHTML = marked.parse(message.dataset.text);
}

async function send_prompt(text) {
    createMessage('user', text);

    chatId = chatId ? chatId : await create_chat();
    const message = await create_message(chatId, text);
    const completion = await create_completion(chatId);
}

async function create_completion(chatId) {
    const body = {
        model: 'google/gemini-3.1-flash-lite',
        effort: 'none'
    };

    const ctrl = new AbortController();

    const assistantMessage = createMessage('assistant');

    await fetchEventSource(`http://localhost:8000/v1/chats/${chatId}/completions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
        signal: ctrl.signal,

        onmessage(ev) {
            messageHandler(ev, assistantMessage);
        },

        onerror(err) {
            throw err;
        }
    });
}

async function messageHandler(ev, message) {
    if (ev.event == 'message') {
        const data = JSON.parse(ev.data);
        updateContent(message, data['chunk']);
    }
}

async function create_chat() {
    const body = {
        user_id: 1
    };

    const response = await fetch('http://localhost:8000/v1/chats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
        console.log('Failed creating chat', data);
        throw new Error('failed creating chat');
    }

    history.pushState(null, '', `/chats/${data['id']}`)

    return data['id'];
}

async function create_message(chatId, text) {
    const body = {
        text: text
    };

    const response = await fetch(`http://localhost:8000/v1/chats/${chatId}/messages`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
        console.log('failed creating message', data);
        throw new Error('Failed creating message');
    }

    return data;
}