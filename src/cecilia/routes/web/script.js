import { fetchEventSource } from 'https://esm.sh/@microsoft/fetch-event-source';

const mainEl = document.querySelector('main');
const messages = document.getElementById('messages');
const prompt = document.getElementById('prompt');
const createNewChat = document.getElementById('create-new-chat');
const navigatorOptions = document.getElementById('chat-nav-options');

// Configs
const uuidReg = /chats\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/
let chatId = window.location.pathname.match(uuidReg)?.[1];
const effortSelector = document.getElementById('prompt-effort');
const modelSelector = document.getElementById('prompt-model');
const attachmentsInput = document.getElementById('prompt-attachments');
const promptAttachmentsContainer = document.getElementById('prompt-attachments-container');
let promptAttachments = [];
const user = get_user_configs();

if (user['effort']) {
    effortSelector.value = user['effort'];
}

if (user['model']) {
    modelSelector.value = user['model'];
}

if (user['id']) {
    // TODO: Pagination with limit + offset
    await buildChats(user['id'], 100, 0);
}

if (chatId) {
    await buildContext(chatId);
    messages.scrollTop = messages.scrollHeight;
}

function get_user_configs() {
    const user = localStorage.getItem('user');

    if (!user) {
        const newUser = {
            id: Math.round(Math.random() * 100000000),
            effort: '',
            model: 'deepseek/deepseek-v4.1-flash'
        }
        localStorage.setItem('user', JSON.stringify(newUser));
        return newUser;
    }

    return JSON.parse(user);
}

function save_user_configs(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// UI
createNewChat.addEventListener('click', (evt) => {
    window.location.href = '/';
});

prompt.addEventListener('keydown', (evt) => {
    if (evt.key != 'Enter' || evt.shiftKey || evt.isComposing) return;

    evt.preventDefault();

    const text = prompt.value.trim();
    if (!text) return;
    sendPrompt(text, promptAttachments);
    attachmentsInput.value = '';
    promptAttachments = [];
    promptAttachmentsContainer.replaceChildren();
    prompt.value = '';
})

attachmentsInput.addEventListener('input', evt => {
    for (const file of evt.target.files) {
        createUserPromptAttachmentEl(promptAttachmentsContainer, file);
    }
});

function createUserPromptAttachmentEl(container, file) {
    const attachment = document.createElement('object');
    const id = Math.round(Math.random() * 10000000);
    attachment.dataset.id = id;
    promptAttachments[id] = file;
    attachment.data = URL.createObjectURL(file);
    attachment.type = file.type;

    attachment.addEventListener('click', evt => {
        promptAttachments.splice(evt.target.dataset.id);
        evt.target.remove();
    });
    container.append(attachment);
}

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
        alert('chat not found');
        window.location.href = '/';
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
        // Process reasoning
        if (extra_data.reasonings) {
            let reasoningText = "";

            extra_data.reasonings.forEach(reasoning => {
                reasoningText += reasoning.text ? reasoning.text : '';
            });

            const [details, summary, content] = createReasoningAddBtn(message);
            updateReasoning(details, content, summary, reasoningText);

            // MessageHeader.append reasoning
        };
    }

    if (role == 'user' && extra_data) {
        if (extra_data.attachments)  {
            extra_data.attachments.forEach(attachment => {
                console.log(attachment);
                const attachmentEl = document.createElement('details');
                attachmentEl.className = 'message__attachment';

                const summary = document.createElement('summary');
                summary.innerHTML = '<span>Open attachment</span>';

                const header = document.createElement('p');
                header.textContent = attachment.public_filename;
                header.className = 'message__attachment__header';

                const mimeType = document.createElement('p');
                mimeType.textContent = attachment.mime_type;
                mimeType.className = 'message__attachment__content';

                attachmentEl.append(summary, header, mimeType);

                message.append(attachmentEl);
                // message header.append
            });
        }
    }

    const contentEl = document.createElement('div');
    contentEl.className = 'message__content';
    contentEl.innerHTML = content ? marked.parse(content) : null;
    
    message.append(contentEl);
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;

    return [message, contentEl];
}

function createReasoningAddBtn(message) {
    const details = document.createElement('details');
    details.className = 'message__reasoning';

    const summary = document.createElement('summary');
    summary.className = 'message__reasoning__summary';

    const summaryTitle = document.createElement('span');
    summaryTitle.textContent = 'Open reasoning';

    const content = document.createElement('div');
    content.className = 'message__reasoning__content';

    summary.append(summaryTitle);
    details.append(summary, content);
    message.prepend(details);

    return [details, summary, content];
}

function updateReasoning(res_el, res_content_el, res_summary_el, text) {
    res_el.dataset.reasoning = res_el.dataset.reasoning ? res_el.dataset.reasoning + text : text;
    res_content_el.innerHTML = marked.parse(res_el.dataset.reasoning);
}

function add_chat_navigation(chatId) {
    const option = document.createElement('li');
    const link = document.createElement('a');
    link.href = `/chats/${chatId}`;
    link.textContent = chatId;

    option.append(link);
    navigatorOptions.append(option);
}

// Logics
async function sendPrompt(text, attachments) {
    createMessageEl('user', text)
    chatId = chatId ? chatId : await createChat();
    const message = await createMessage(chatId, text);
    await createAttachments(chatId, message['id'], attachments);
    const completion = await createCompletion(chatId);
}

async function createChat() {
    const body = {
        user_id: user['id']
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
        alert('Failed creating the chat');
        throw new Error('failed creating chat');
    }

    history.pushState(null, '', `/chats/${data['id']}`);
    add_chat_navigation(data['id']);
    return data['id'];
}

async function createAttachments(chatId, messageId, attachments) {
    if (!attachments.length > 0) {
        console.log('length');
        return;
    }

    const formData = new FormData();

    attachments.forEach(attachment => {
        formData.append('files', attachment); // TODO: Substituir o new File para usar o objeto attachments diretamente, pois ele ja 'e file
    });

    const response = await fetch(`/v1/chats/${chatId}/messages/${messageId}/attachments`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        console.log(await response.json());
        alert(`Failed uploading attachments`);
    }

    console.log(await response.json());

    return ;
}

async function createMessage(chatId, text) {
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
        alert('Failed creating message');
        throw new Error('Failed creating message');
    }

    return data;
}

async function createCompletion(chatId) {
    user['effort'] = effortSelector.value;
    user['model'] = modelSelector.value;
    save_user_configs(user);

    const body = {
        model: modelSelector.value,
        effort: effortSelector.value === '' ? null : effortSelector.value
    };

    const ctrl = new AbortController();
    const [assistantMessage, assistantContent] = createMessageEl('assistant');
    let [reasoningEl, summaryEl, contentEl] = [];

    await fetchEventSource(`/v1/chats/${chatId}/completions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
        signal: ctrl.signal,

        onmessage(ev) {
            if (ev.event == 'reasoning' && !reasoningEl) {
                [reasoningEl, summaryEl, contentEl] = createReasoningAddBtn(assistantMessage);
            }
            messageHandler(ev, assistantContent, assistantMessage, reasoningEl, summaryEl, contentEl);
        },

        onerror(err) {
            throw err;
        }
    });
}

async function messageHandler(ev, content, message, reasoningEl, summaryEl, contentEl) {
    const data = JSON.parse(ev.data);
    if (ev.event == 'message') {
        updateContent(content, data['chunk']);
    }

    if (ev.event == 'reasoning' && reasoningEl) {
        updateReasoning(reasoningEl, contentEl, summaryEl, data['reasoning'].join('\n\n'));
    }

    if (ev.event == 'error') {
        console.log('stream error: ', data);
        updateContent(content, `# Error - ${data['title']} \n\n ${data['message']}`);
    }
}

function updateContent(content, text) {
    content.dataset.text = content.dataset.text ? content.dataset.text + text : text;
    content.innerHTML = marked.parse(content.dataset.text);
}