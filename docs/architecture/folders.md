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

## Extractors

- Extraem dados de algo

## Adapters

- Adaptam uma comunicação externa para o modelo interno

## Integrations

- Se integram a algo externo e o adapta para a estrutura de comunicação interna

## Policies

- Aplicam regras de negocio para a ação específica

## Services

- Aplicam regras de negocio imutáveis.
- Se comunicam com seu proprio repository.
- Se precisarem de dados de outro service, um use case deve os fornecer.
- Internos (Evitar chamar diretamente)

## Use cases

- Recebem os dados
- Validam os dados (com BaseModel)
- Coletam oq for necessario para uma acao.
- Chamam oq for necessario para a acao
- Representam uma acao especifica

## Models

- Representam a tabela
- Tem classes de dados

## Repositories

- Se comunicam com a ORM na sua model especifica
- Sem regras de negocio
- Expoem metodos simples

## Controllers

- Recebem o request das rotas de API
- Chamam os use cases

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

## Builders

- Pegam um input e o constroi no formato necessário
