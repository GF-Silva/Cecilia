import { fetchEventSource } from 'https://esm.sh/@microsoft/fetch-event-source';

const mainEl = document.querySelector('main');
const messages = document.getElementById('messages');
const prompt = document.getElementById('prompt');
const createNewChat = document.getElementById('create_new_chat');
const navigatorOptions = document.getElementById('chat_nav__options');
const uuidReg = /chats\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/
let userId = get_user_id();
let chatId = window.location.pathname.match(uuidReg)?.[1];

if (chatId) {
    await buildContext(chatId);
    messages.scrollTop = messages.scrollHeight;
}

if (userId) {
    // TODO: Pagination with limit + offset
    await buildChats(userId, 100, 0);
}

function get_user_id() {
    // Pega o user salvo
    const user = localStorage.getItem('user');

    // N tem user, cria novo
    if (!user) {
        // cria o novo user
        const newUserId = Math.round(Math.random() * 1000000000);
        localStorage.setItem('user', JSON.stringify({
            id: newUserId
        }));
        return newUserId;
    }
    
    return JSON.parse(user)['id'];
}

createNewChat.addEventListener('click', (evt) => {
    window.location.href = '/';
});

prompt.addEventListener('keydown', (evt) => {
    if (evt.key != 'Enter' || evt.shiftKey || evt.isComposing) return;

    evt.preventDefault();

    const text = prompt.value.trim();

    if (!text) return;

    send_prompt(text);

    prompt.value = '';
})

async function buildChats(userId, limit, offset) {
    const response = await fetch(`/v1/chats/${userId}?limit=${limit}&offset=${offset}`);

    if (!response.ok) {
        throw new Error('Error getting user chats');
    }

    const data = await response.json();

    data.forEach(chat => {
        add_chat_navigation(chat['id']);
    });
}

async function buildContext(chatId) {
    const response = await fetch(`/v1/chats/${chatId}/messages`);

    if (!response.ok) {
        throw new Error('Falha iniciando context');
    }

    const data = await response.json();

    data.forEach(msg => {
        createMessageEl(msg['is_user'] ? 'user' : 'assistant', msg['text'], msg);
    });
}

function createMessageEl(role, content, extra_data) {
    const message = document.createElement('div');
    message.className = `message ${role == 'user' ? 'message__user' : 'message__assistant'}`;

    if (role == 'assistant' && extra_data) {
        // Process reasonings
        if (extra_data['reasonings']) {
            extra_data['reasonings'].forEach(reasoning => {    
                if (reasoning.text) {
                    message.dataset.reasoning = message.dataset.reasoning ? message.dataset.reasoning + reasoning.text : reasoning.text;
                    const reasoningOpener = document.createElement('button');
                    reasoningOpener.className = 'open_reasoning';
                    reasoningOpener.addEventListener('click', _ => {
                        createDisplay('Reasoning', marked.parse(message.dataset.reasoning));
                    });

                    message.append(reasoningOpener);
                }
            });
        };
    }

    const text = document.createElement('p');
    text.innerHTML = content ? marked.parse(content) : null;

    message.append(text);
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;

    return message;
}

function createDisplay(title, content) {
    const display = document.createElement('div');
    display.className = 'display';

    const titleEl = document.createElement('h2');
    titleEl.textContent = title;
    display.append(titleEl);

    const displayContent = document.createElement('div');
    displayContent.className = 'display__content';
    displayContent.innerHTML = content
    display.append(displayContent);

    mainEl.append(display);
}

function updateContent(message, text) {
    message.dataset.text = message.dataset.text ? message.dataset.text + text : text;
    message.innerHTML = marked.parse(message.dataset.text);
}

async function send_prompt(text) {
    createMessageEl('user', text);

    chatId = chatId ? chatId : await create_chat();
    const message = await create_message(chatId, text);
    const completion = await create_completion(chatId);
}

async function create_completion(chatId) {
    const body = {
        model: 'google/gemini-3.1-flash-lite',
        effort: 'medium'
    };

    const ctrl = new AbortController();

    const assistantMessage = createMessageEl('assistant');

    await fetchEventSource(`/v1/chats/${chatId}/completions`, {
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
    const data = JSON.parse(ev.data);
    console.log(data);
    if (ev.event == 'message') {
        updateContent(message, data['chunk']);
    }

    if (ev.event == 'reasoning') {
        console.log(data['reasonings'])
    }
}

async function create_chat() {
    const body = {
        user_id: userId
    };

    const response = await fetch('/v1/chats', {
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

    history.pushState(null, '', `/chats/${data['id']}`);
    add_chat_navigation(data['id']);
    return data['id'];
}

function add_chat_navigation(chatId) {
    const option = document.createElement('li');
    const link = document.createElement('a');
    link.href = `/chats/${chatId}`;
    link.textContent = chatId;

    option.append(link);
    navigatorOptions.append(option);
}

async function create_message(chatId, text) {
    const body = {
        text: text
    };

    const response = await fetch(`/v1/chats/${chatId}/messages`, {
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