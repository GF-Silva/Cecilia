# Attachments in chats planning

Here is the planning of that should or should not be done to add the attachments feature

## Context

### Dor

Os usuarios não podem fazer upload de arquivos de audio e texto para o assistente.
O assistente não pode retornar arquivos de aúdio para o usuário

### Escopo

Um sistema para o usuario enviar arquivos de audio e image para o assistente, que aceita apenas arquivos integros.
Não terá upload de outros tipos de arquivo, nem retorno de mensagens de audio ou imagem vindos do assistente.

### Requisitos

#### Funcionais

1. CRUD De arquivos de audio e imagem, apenas.
2. Persistir esses arquivos (no banco de dados e em um object storage).
3. Retornar esses arquivos quando buscar o contexto do chat.
4. Enviar esses arquivos para o assistente processar.
5. O usuário só pode criar um attachment para mensagens dele mesmo.
6. O assistant não pode criar attachments.
7. O arquivo deve ser válido (Integro).
8. Um attachment não deve existir sem uma mensagem
9. O sistema deve aceitar apenas imagens de até 20MB.
10. O sistema deve aceitar apenas aúdios de até 100MB.
11. Os dados como tamanho, mime type e nome devem ser salvos.
12. O sistema deve validar o input dos dados
13. O sistema deve recusar a criação para uma mensagem inexistente
14. O sistema deve criar e salvar apenas os arquivos validos
15. O sistema deve mostrar quais arquivos estão inválidos e foram recusados
16. O sistema deve ter um meio de invalidar arquivos já criados
17. O usuário só pode criar um attachment para seu proprio chat e mensagem

#### Não funcionais

- A validação de arquivos deve ser assíncrona
- Os arquivos devem ser validados de forma paralela

### Ações

#### Criar os arquivos

- Verificar se a mensagem em que o usuário quer criar o attachment é dele
- Verificar se o message alvo não é do assistant
- Verificar se é realmente um usuário solicitando a criação do attachment
- Validar se os dados enviados são válidos
- Validar o arquivo
- Criar os arquivos no database
- Criar os arquivos no object storage
- Verificar se a mensagem existe
- Salvar o tamanho, mime_type e filename
- Verificar se os dados enviados são válidos
- Salvar apenas os arquivos validos
- Retornar os arquivos que derem erro

#### Atualizar os arquivos

- Verificar se a mensagem em que o usuário quer atualizar o attachment é dele
- Verificar se o message alvo não é do assistant
- Verificar se é realmente um usuário solicitando a atualização do attachment
- Validar se os dados enviados são válidos
- Validar o arquivo
- Atualizar os arquivos no database
- Atualizar os arquivos no object storage
- Verificar se a mensagem existe
- Atualizar o tamanho, mime_type e filename
- Verificar se os dados enviados são válidos
- Atualizar apenas os arquivos validos
- Retornar os arquivos que derem erro
- O attachment não pode ter sido deletado ou invalidado

#### Obter arquivos

- Verificar se quem está pedindo é o dono do attachment.
- Recuperar os dados do attachment do database
- Verificar se o attachment existe
- O attachment não pode ter sido deletado ou invalidado

#### Deletar arquivos

- Verificar se quem está pedindo é o dono do attachment.
- Recuperar os dados do attachment do database
- Verificar se o attachment existe
- Invalidar o attachment no database
- Invalidar o attachment no object storage (Ou remover ele, como medida temporaria)
- O attachment não pode ter sido deletado ou invalidado anteriormente

#### Criar completion

- Verificar se o usuário é o dono daquele chat
- Buscar as mensagens do chat
- Buscar os attachments
- Formatar os attachments com a estrutura da openrouter
- Se necessario, gerar o link de referência ou arquivo decodificado para enviar
- Enviar as mensagens para a integration do openrouter
- Retornar a resposta em stream
- Verificar se o chat tem mensagens registradas
- Os attachments da mensagem não podem ter sido deletado ou invalidado

#### Validar o arquivo

- Validar o mime type do arquivo
- Validar se a estrutura está integra
- Verificar se o tamanho não passa do máximo (20MB para imagens, 100MB para audios)
- Retornar os dados dos arquivos válidos
- Retornar quais arquivos falharam na validação

#### Invalidar o arquivo já criado

- Recebe o ID do attachment
- Obtem o attachment do database
- Atualiza os campos necessarios para marcar o attachment como invalido
- O attachment buscado deve existir
- O attachment não pode ter sido deletado ou invalidado

## Regras por ação

### Ação de criar arquivos

- **Usuário:** Cliente

#### Regras gerais de criar

- O usuário só pode criar um attachment em suas próprias mensagens
- Um attachment só pode ser criado por usuários (Não assistant)
- Os dados de entrada devem ser válidos
- O arquivo deve estar integro
- A mensagem deve existir para criar um attachment
- Um attachment só existe enquanto sua mensagem existir
- Apenas os arquivos válidos devem ser salvos
- Os arquivos inválidos devem ser retornados

#### Regras imutáveis de criar

- Os dados de entrada devem ser válidos
- O arquivo deve estar integro
- A mensagem deve existir para criar um attachment
- Um attachment só existe enquanto sua mensagem existir
- Apenas os arquivos válidos devem ser salvos
- Os arquivos inválidos devem ser retornados

#### Regras específicas de criar

- O usuário só pode criar um attachment em suas próprias mensagens
- Um attachment só pode ser criado por usuários (Não assistant)

### Ação de Atualizar os arquivos

**Usuário:** Cliente

#### Regras gerais de atualizar

- O attachment não pode ter sido deletado ou invalidado
- A mensagem (atual e alvo) deve ser do usuário para ele atualizar o attachment
- O attachment deve ser do usuário para ele atualizar ele
- Os novos dados enviados para atualizar devem ser validos
- O arquivo novo enviado deve ser valido
- O id da mensagem alvo deve existir
- Atualizar apenas se os arquivos forem validos
- Retornar os arquivos que derem erro

#### Regras imutáveis de atualizar

- Os novos dados enviados para atualizar devem ser validos
- O arquivo novo enviado deve ser valido
- O id da mensagem alvo deve existir
- Atualizar apenas se os arquivos forem validos
- Retornar os arquivos que derem erro

#### Regras específicas de atualizar

- O attachment não pode ter sido deletado ou invalidado
- A mensagem (atual e alvo) deve ser do usuário para ele atualizar o attachment
- O attachment deve ser do usuário para ele atualizar ele

### Ação de Obter arquivos

**Usuário:** Cliente, sistema

#### Regras gerais de obter arquivos

- O attachment não pode ter sido deletado ou invalidado
- Aquele que pede deve ser o dono do attachment.
- O sistema só deve pegar um attachment quando o comando for de interesse e objetivo do usuário.
- O sistema só pode pegar um attachment para usuário que for o dono desse mesmo attachment.
- Verificar se o attachment existe

#### Regras imutáveis de obter arquivos

- Verificar se o attachment existe

#### Regras específicas de obter arquivos

- Aquele que pede deve ser o dono do attachment.
- O sistema só deve pegar um attachment quando o comando for de interesse e objetivo do usuário.
- O sistema só pode pegar um attachment para usuário que for o dono desse mesmo attachment.
- O attachment não pode ter sido deletado ou invalidado

### Ação de Deletar arquivos

- **Usuário:** Cliente, sistema

#### Regras gerais de deletar arquivos

- Quem pede a ação deve ser o dono do attachment.
- O sistema só pode deletar attachments com o pedido do usuário.
- O sistema só pode deletar attachments do mesmo usuário que o pediu.
- Um attachment precisa existir para ser deletado.

#### Regras imutáveis

- Um attachment precisa existir para ser deletado.

#### Regras específicas

- Quem pede a ação deve ser o dono do attachment.
- O sistema só pode deletar attachments com o pedido do usuário.
- O sistema só pode deletar attachments do mesmo usuário que o pediu.

### Ação de Criar completion

- **Usuário:** Cliente

#### Regras gerais de criar completion

- Os attachments da mensagem não podem ter sido deletado ou invalidado
- Aquele que pede a ação deve ser o dono do chat.
- O chat deve ter mensagens

#### Regras imutáveis de criar completion

- O chat deve ter mensagens
- Os attachments da mensagem não podem ter sido deletado ou invalidado

#### Regras específicas de criar completion

- Aquele que pede a ação deve ser o dono do chat.

### Ação de Validar o arquivo

- **Usuário:** Sistema

#### Regras gerais feitas ao validar um arquivo

- O mime type deve ser aceito (Audio ou imagem)
- A estrutura do arquivo deve estar integra
- O arquivo não pode ser vazio
- Deve respeitar um tamanho máximo (20MB para imagens, 100MB para audios)

#### Regras imutáveis para validar um arquivo

- A estrutura do arquivo deve estar integra

#### Regras específicas para validar um arquivo

- O arquivo não pode ser vazio
- Deve respeitar um tamanho máximo (20MB para imagens, 100MB para audios)
- O mime type deve ser aceito (Audio ou imagem)

### Ação de Invalidar o arquivo já criado

- **Usuário:** Sistema, cliente

#### Regras gerais de invalidar o arquivo já arquivo criado

- O attachment buscado deve existir
- O usuário deve ser o dono do attachment
- O attachment não pode ter sido deletado ou invalidado

#### Regras imutaveis de invalidar o arquivo já arquivo criado

- O attachment buscado deve existir
- O attachment não pode ter sido deletado ou invalidado

#### Regras específicas de invalidar o arquivo já criado

- O usuário deve ser o dono do attachment

## Definição das responsabilidades

### Definição dos agentes

1. AttachmentService
2. AttachmentRepository
3. AttachmentModel
4. AttachmentImageValidationPolicy.
5. AttachmentAudioValidationPolicy.
6. AttachmentValidationPolicyDispatcher
7. AttachmentAccessPolicy
8. OpenRouterCompletionsIntegration
9. MessageService
10. ChatService
11. ImageValidator
12. AudioValidator
13. FileMetadataExtractor
14. R2Integration
15. DatabaseToOpenRouterMessageBuilder
16. AttachmentCreateUseCase
17. AttachmentUpdateUseCase
18. AttachmentAccessUseCase
19. AttachmentDeleteUseCase
20. MessageAccessPolicy
21. ChatAccessPolicy

### Agrupamento das regras

- [Policies](policies.md)           -- Feito
- [Dispatchers](dispatchers.md)     -- Feito
- [Extractors](extractors.md)       -- Fazendo
- [Validators](validators.md)
- [UseCases](use_cases.md)
- [Builders](builders.md)
- [Integrations](integrations.md)
- [Services](services.md)
- [Repositories](repositories.md)
- [Models](models.md)
