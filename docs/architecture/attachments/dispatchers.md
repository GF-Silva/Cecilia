# Dispatchers

## AttachmentValidationPolicyDispatcher

### Regras ao dispachar uma validation

- O mime type deve ser aceito (Audio ou image)

### Ações ao dispachar uma validation

- Receber o MimeType
- Comparar o MimeType com as opções disponíveis de regras de validação
- Dispachar o request para a opção certa
- Se não tiver nenhuma opção, retornar erro de formato não suportado
