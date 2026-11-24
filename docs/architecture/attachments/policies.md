# Policies

## AttachmentAccessPolicy

### Regras no acesso

- Aquele que acessa deve ser o dono do attachment
- Um attachment só pode ser criado por usuários (Não assistant)

### Ações no acesso

- Validar se quem solicita modificar um attachment pode criar um
- Verificar se o role é válido e pode acessar o attachment
- Verificar se quem pede é o dono do attachment

## MessageAccessPolicy

### Regras do acesso às mensagens

- O usuario acessa apenas as mensagens de seu proprio chat
- Seu chat acessa apenas suas proprias mensagens
- A mensagem (atual e alvo) deve ser do usuário
- O user só pode acessar manipular attachments de suas mensagens

### Ações no acesso em mensagens

- Verificar se o Role da mensagem é o mesmo role de quem chama
- Verificar se o chat pode acessar essa mensagem
- Verificar se quem quer acessar é o dono da mensagem

## ChatAccessPolicy

### Regras do acesso ao chat

- O usuário acessa apenas seu proprio chat

### Ações ao validar o acesso a um chat

- Verificar se quem pede é um usuário
- Verificar se quem pede é o dono do item
