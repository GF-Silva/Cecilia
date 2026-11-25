# Validators

## ImageValidator

### Regras ao validar uma imagem

- A imagem deve ter a estrutura valida.

### Ações ao validar uma imagem

- Usar o `Pillow` para validar a imagem
- Retornar se deu certo ou errado

## AudioValidator

### Regras ao validar um audio

- O áudio deve ter a estrutura valida.

### Ações ao validar a integridade um audio

- Usar o `FFProbeAdapter` para validar o audio
- Retornar se deu certo ou errado

## AttachmentImageValidationPolicy

### Regras de negócio ao validar uma imagem

- O arquivo deve estar integro
- O tamanho máximo deve ser 20MB

### Ações ao validar a política de uma imagem

- Chamar o `ImageValidator` para verificar se a mensagem é valida
- Verificar o tamanho
- Verificar a estrutura interna
- Verificar a segurança do item
- Retornar se o arquivo deu certo ou errado

## AttachmentAudioValidationPolicy

### Regras de negócio ao validar um audio

- O arquivo deve estar integro
- O tamanho máximo deve ser 100MB

### Ações ao validar um audio

- Chamar o `AudioValidator` para verificar se a mensagem é valida
- Verificar o tamanho
- Verificar a estrutura interna
- Verificar a segurança do item
- Retornar se o arquivo deu certo ou errado
