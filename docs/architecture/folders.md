# Folders structure

Here is the folder structure that will be used.
Notice that they are for me to follow this architecture, so can be classified as internal and i do not provide a english version.

## Ordem de uso para uma ação de rota

1. Controllers
2. Use case
3. Services
4. Repository
5. Models

## Validators

- Recebem um item
- Validam apenas a integridade desse item
- Não aplicam regras de negocio
- O nome é Type + Validator. Ex: ImageValidator

## Extractors

- Extraem dados de algo
- O nome é Type + What + Extractor. Ex: FileMetadataExtractor

## Adapters

- Adaptam uma comunicação externa para o modelo interno
- O nome é Domain + Adapter. Ex: FFProbeAdapter

## Integrations

- Se integram a algo externo e o adapta para a estrutura de comunicação interna
- O nome é Domain + Action + Integration. Ex: OpenRouterCompletionsIntegration

## Dispatcher

- Deve ser criado 1 para cada ação (Ex: create attachment)
- Redirecionam a chamada para o item certo
- O nome é Domain + Action + Context + Dispatcher. Ex: AttachmentCreatePolicyDispatcher

## Validation Policies

- Aplicam regras de negocio de validação para o tipo específico.
- O nome é Domain + Type + Validation + Policy. Ex: AttachmentImageValidationPolicy

## Access Policies

- Aplicam regras de acesso para o item especifico
- O nome é Domain + Access + Policy. Ex: AttachmentAccessPolicy.

## Services

- Aplicam regras de negocio imutáveis.
- Se comunicam com seu proprio repository.
- Se precisarem de dados de outro service, um use case deve os fornecer.
- Internos (Evitar chamar diretamente)
- O nome é Domain + Service. Ex: AttachmentService

## Use cases

- Recebem os dados
- Validam os dados (com BaseModel)
- Coletam oq for necessario para uma acao.
- Chamam oq for necessario para a acao
- Representam uma acao especifica
- O nome é Domain + Action + UseCase. Ex: AttachmentCreateUseCase

## Models

- Representam a tabela
- Tem classes de dados
- O nome é Domain + Action. Ex: AttachmentUpdate

## Repositories

- Se comunicam com a ORM na sua model especifica
- Sem regras de negocio
- Expoem metodos simples
- O nome é Domain + Repository. Ex: AttachmentRepository

## Controllers

- Recebem o request das rotas de API
- Chamam os use cases
- O nome é Domain + Controller. Ex: AttachmentController

## Core

- Arquivos globais
- Configurações
- Genérico

## Routes

- Expõem rotas HTTP
- Chamam use cases

## Collectors

- Pegam um stream de itens
- Constroem esses itens no formato necessário
- O nome é Domain + Action + Collector. Ex: OpenRouterCompletionsCollector

## Builders

- Pegam um input e o constroi no formato necessário
- O nome é DomainInputItem + To + DomainOutputItem + Builder. Ex: DatabaseToOpenRouterMessageBuilder
