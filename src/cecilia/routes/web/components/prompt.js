export class Prompt {
    constructor (container, onPromptSend, effortOptions) {
        this.effortOptions = effortOptions;

        const promptContainer = document.createElement('div');
        promptContainer.className = 'prompt__container';

        const attachments = document.createElement('div');
        attachments.className = 'prompt__container__attachments';
        attachments.id = 'prompt-attachments-container';

        const [ promptAttachmentsInput ] = this.createPromptOptions(promptContainer);

        const prompt = document.createElement('textarea');
        prompt.id = 'prompt';
        prompt.className = 'prompt';
        prompt.placeholder = 'What do you want to do?';

        let promptAttachments = [];
        
        prompt.addEventListener('keydown', async (evt) => {
            if (evt.key != 'Enter' || evt.shiftKey || evt.isComposing) return;
            evt.preventDefault();

            const text = prompt.value.trim();
            if (!text) return;
            
            await onPromptSend(text, promptAttachments);
            promptAttachmentsInput.value = '';
            promptAttachments = [];
            attachments.replaceChildren();
            prompt.value = '';
        });

        promptContainer.append(attachments, prompt);
        container.append(promptContainer);

        return [ promptAttachments ];
    }

    createPromptOptions(container) {
        const promptOptions = document.createElement('div');
        promptOptions.setAttribute('popover', 'auto')
        promptOptions.id = 'prompt__options';

        const effortSelectorEl = document.createElement('select');
        effortSelectorEl.name = 'effort';
        effortSelectorEl.id = 'prompt-effort';

        for (const effort in this.effortOptions) {
            const opt = document.createElement('option');
            opt.value = effort;
            opt.textContent = this.effortOptions[effort];
            effortSelectorEl.append(opt);
        }

        const effortSelectorContainer = document.createElement('div');
        effortSelectorContainer.innerHTML = '<label for="prompt-effort">Effort: </label>';
        effortSelectorContainer.append(effortSelectorEl);

        promptOptions.innerHTML = `
            <label for="prompt-attachments" class="prompt__options__upload-attachment__label">Upload file</label>
            
            <div>
                <label for="prompt-model">Model: </label>
                <select name='model' class="prompt-model" id='prompt-model'>
                    <option value="google/gemini-3.1-flash-lite">Gemini 3.1 Flash Lite</option>
                    <option value="deepseek/deepseek-v4.1-flash">DeepSeek V4.1 Flash</option>
                    <option value="~anthropic/claude-opus-latest">Claude Opus lastest</option>
                    <option value="anthropic/claude-opus-5.5">Claude Opus 5.5</option>
                    <option value="anthropic/claude-sonnet-5.5">Claude Sonnet 5.5</option>
                    <option value='anthropic/claude-haiku-5.5'>Claude Haiku 5.5</option>
                    <option value="anthropic/claude-fable-5.2">Claude Fable 5.2</option>
                    <option value="openai/gpt-4">GPT 4</option>
                    <option value="openai/gpt-6.1-sol">GPT 6.1 Sol</option>
                    <option value="openai/gpt-6-astra">GPT 6 Astra</option>
                    <option value="openai/gpt-6.1-terra">GPT 6.1 Terra</option>
                    <option value="openai/gpt-6-luna">GPT 6 Luna</option>
                </select>
            </div>
        `;

        promptOptions.append(effortSelectorContainer);

        const promptAttachmentsInput = document.createElement('input');
        promptAttachmentsInput.accept = 'image/*; audio/*';
        promptAttachmentsInput.type = 'file';
        promptAttachmentsInput.name = 'Upload attachment';
        promptAttachmentsInput.id = 'prompt-attachments';
        promptAttachmentsInput.hidden = true;
        promptAttachmentsInput.multiple = true;

        promptOptions.append(promptAttachmentsInput);

        const optionsOpenerBtn = document.createElement('button');
        optionsOpenerBtn.popoverTargetElement = promptOptions;
        optionsOpenerBtn.className = 'prompt__options__opener';
        optionsOpenerBtn.ariaHasPopup = 'menu';
        optionsOpenerBtn.textContent = '+';

        container.append(optionsOpenerBtn, promptOptions, promptAttachmentsInput);

        return [ promptAttachmentsInput ];
    }
}