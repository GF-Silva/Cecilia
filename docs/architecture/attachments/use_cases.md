# UseCases

## OpenRouterCompletionsCreateUseCase

### Regras ao criar uma completion

- O chat deve ter mensagens

### Ações ao criar uma completion

- Receber o id do user e chat
- Chamar o `AttachmentAccessPolicy` para verificar se o user pode acessar o attachment ---- (Maybe not)
- Chamar o `MessageAccessPolicy` para verificar se o user pode acessar a mensagem
- Chamar o `ChatAccessPolicy` para verificar se o user pode acessar o chat
- Chamar o `MessageService` para obter as mensagens do chat
- Verificar se o chat tem mensagens
- Chamar o `DatabaseToOpenRouterMessageBuilder` para transformar as mensagens no modelo do openrouter
- Enviar as mensagens para o `OpenRouterCompletionsIntegration` processar
- Retornar a resposta em stream

## AttachmentCreateUseCase

### Regras ao criar um attachment

- Criar apenas se os arquivos forem validos
- Retornar os arquivos que derem erro
- O arquivo não pode ser vazio

### Ações ao criar um attachment

- Chamar o `ChatAccessPolicy` para validar se o user_id pode acessar o chat
- Chamar o `MessageAccessPolicy` para validar se o user pode acessar a mensagem desse chat
- Chamar o `AttachmentAccessPolicy` para validar se o usuário pode executar a ação
- Chamar o `FileMetadataExtractor` para extrar o mime type
- Chamar o `AttachmentValidationPolicyDispatcher` para validar os arquivos
- Chamar o `AttachmentService` para criar o attachment no database
- Chamar a `R2Integration` para criar o attachment no database
- Retornar os dados dos arquivos que deram certo na validação
- Retornar os dados dos arquivos que deram errado na validação
- Salvar os arquivos válidos

## AttachmentUpdateUseCase

### Regras ao atualizar um attachment

- Atualizar apenas se os arquivos forem validos
- Retornar os arquivos que derem erro
- O arquivo não pode ser vazio

### Ações ao atualizar um attachment

- Chamar o `AttachmentValidationPolicyDispatcher` para validar os arquivos
- Chamar o `FileMetadataExtractor` para extrar o mime type
- Chamar o `AttachmentAccessPolicy` para verificar se o user pode acessar o attachment
- Chamar o `MessageAccessPolicy` para verificar se o user pode acessar a mensagem
- Chamar o `ChatAccessPolicy` para verificar se o user pode acessar o chat
- Chamar o `AttachmentService` para pegar os dados de um attachment
- Retornar os dados dos arquivos que deram certo na validação
- Retornar os dados dos arquivos que deram errado na validação
- Salvar os arquivos válidos

## AttachmentAccessUseCase

### Ações ao acessar um attachment

- Chamar a `AttachmentShowFacade` para validar a permissao de show
- TODO: Se for buscar os dados do arquivo no database, chamar a `R2Integration` para buscar o arquivo no database

## AttachmentDeleteUseCase

### Ações ao deletar um attachment

- Chamar o `AttachmentService` para marcar o attachment como inválido
- Chamar o `AttachmentAccessPolicy` para verificar se o user pode acessar o attachment
- Chamar o `MessageAccessPolicy` para verificar se o user pode acessar a mensagem
- Chamar o `ChatAccessPolicy` para verificar se o user pode acessar o chat
- Chamar a `R2Integration` para deletar a mensagem
