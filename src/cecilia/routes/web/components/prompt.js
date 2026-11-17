export class Prompt {
    constructor (container, onPromptSend, effortOptions, modelOptions) {
        this.effortOptions = effortOptions;
        this.modelOptions = modelOptions;

        const promptContainer = document.createElement('div');
        promptContainer.className = 'prompt__container';

        const attachments = document.createElement('div');
        attachments.className = 'prompt__container__attachments';
        attachments.id = 'prompt-attachments-container';

        const [ promptAttachmentsInput ] = this.createPromptOptions(promptContainer, modelOptions);

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

        promptOptions.innerHTML = `
            <label for="prompt-attachments" class="prompt__options__upload-attachment__label">Upload file</label>
        `;
        
        this.createEffortSelector(promptOptions);
        this.createModelSelector(promptOptions);
        const promptAttachmentsInput = this.createAttachmentInput(promptOptions);

        const optionsOpenerBtn = document.createElement('button');
        optionsOpenerBtn.popoverTargetElement = promptOptions;
        optionsOpenerBtn.className = 'prompt__options__opener';
        optionsOpenerBtn.ariaHasPopup = 'menu';
        optionsOpenerBtn.textContent = '+';

        container.append(optionsOpenerBtn, promptOptions);

        return [ promptAttachmentsInput ];
    }

    createAttachmentInput(container) {
        const promptAttachmentsInput = document.createElement('input');
        promptAttachmentsInput.accept = 'image/*; audio/*';
        promptAttachmentsInput.type = 'file';
        promptAttachmentsInput.name = 'Upload attachment';
        promptAttachmentsInput.id = 'prompt-attachments';
        promptAttachmentsInput.hidden = true;
        promptAttachmentsInput.multiple = true;

        container.append(promptAttachmentsInput);

        return promptAttachmentsInput;
    }

    createEffortSelector(container) {
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
        container.append(effortSelectorContainer);
    }

    createModelSelector(container) {
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
        container.append(selectorContainerEl);
    }
}