export class Prompt {
    constructor (container, onPromptSend, effortOptions, modelOptions) {
        this.onPromptSend = onPromptSend;
        this.effortOptions = effortOptions;
        this.modelOptions = modelOptions;
        this.promptAttachments = [];

        const promptContainer = document.createElement('div');
        promptContainer.className = 'prompt__container';

        this.attachments = document.createElement('div');
        this.attachments.className = 'prompt__container__attachments';
        this.attachments.id = 'prompt-attachments-container';

        const [ optionsOpenerBtn, promptOptions ] = this.createPromptOptions(promptContainer, modelOptions);
        const effortSelector = this.createEffortSelector();
        const modelSelector = this.createModelSelector();
        const promptAttachmentsInput = this.createAttachmentInput();
        const prompt = this.createPromptInput(promptAttachmentsInput);

        promptOptions.append(effortSelector, modelSelector, promptAttachmentsInput)
        promptContainer.append(promptOptions, optionsOpenerBtn, this.attachments, prompt);
        container.append(promptContainer);
    }

    createPromptInput(promptAttachmentsInput) {
        const prompt = document.createElement('textarea');
        prompt.id = 'prompt';
        prompt.className = 'prompt';
        prompt.placeholder = 'What do you want to do?';
        
        prompt.addEventListener('keydown', async (evt) => {
            if (evt.key != 'Enter' || evt.shiftKey || evt.isComposing) return;
            evt.preventDefault();

            const text = prompt.value.trim();
            if (!text) return;
            promptAttachmentsInput.value = '';
            this.attachments.replaceChildren();
            prompt.value = '';
            
            await this.onPromptSend(text, this.promptAttachments);
            this.promptAttachments = [];
        });

        return prompt;
    }

    createPromptOptions() {
        const promptOptions = document.createElement('div');
        promptOptions.setAttribute('popover', 'auto')
        promptOptions.id = 'prompt__options';

        promptOptions.innerHTML = `
            <label for="prompt-attachments" class="prompt__options__upload-attachment__label">Upload file</label>
        `;

        const optionsOpenerBtn = document.createElement('button');
        optionsOpenerBtn.popoverTargetElement = promptOptions;
        optionsOpenerBtn.className = 'prompt__options__opener';
        optionsOpenerBtn.ariaHasPopup = 'menu';
        optionsOpenerBtn.textContent = '+';

        return [ optionsOpenerBtn, promptOptions ];
    }

    createAttachmentInput() {
        const promptAttachmentsInput = document.createElement('input');
        promptAttachmentsInput.accept = 'image/*; audio/*';
        promptAttachmentsInput.type = 'file';
        promptAttachmentsInput.name = 'Upload attachment';
        promptAttachmentsInput.id = 'prompt-attachments';
        promptAttachmentsInput.hidden = true;
        promptAttachmentsInput.multiple = true;

        return promptAttachmentsInput;
    }

    createEffortSelector() {
        const effortSelectorContainer = document.createElement('div');

        // Seletor de effort
        const selectorEl = document.createElement('select');
        selectorEl.name = 'effort';
        selectorEl.id = 'prompt-effort';

        // Seletor de label
        const label = document.createElement('label');
        label.for = 'prompt-effort';
        label.textContent = 'Effort: ';

        for (const effort in this.effortOptions) {
            const opt = document.createElement('option');
            opt.value = effort;
            opt.textContent = this.effortOptions[effort];
            selectorEl.append(opt);
        }

        effortSelectorContainer.append(label, selectorEl);
        return effortSelectorContainer;
    }

    createModelSelector() {
        const selectorContainerEl = document.createElement('div');

        const label = document.createElement('label');
        label.for = 'prompt-model';
        label.textContent = 'Model: ';

        const modelSelector = document.createElement('select');
        modelSelector.name = 'model';
        modelSelector.class = 'prompt-model';
        modelSelector.id = 'prompt-model';

        for (const model in this.modelOptions) {
            const opt = document.createElement('option');
            opt.value = model;
            opt.textContent = this.modelOptions[model];
            modelSelector.append(opt);
        }

        selectorContainerEl.append(label, modelSelector);
        return selectorContainerEl;
    }
}