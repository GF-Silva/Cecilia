# Policies

## AttachmentAccessPolicy

### Regras no acesso

- Apenas o usuário dono da mensagem acessa o attachment
- Para modificar, o role do usuário deve ser o mesmo da mensagem alvo
- Aquele que acessa deve ser o dono do attachment
- Apenas users podem acessar

### Ações no acesso

- Validar a permissão para manipular um attachment
- Para criar ou atualizar, validar se o role é de um usuário
- Para criar ou atualizar, verificar se o role da mensagem alvo é o mesmo role de quem pede a ação
- Verificar se quem pede é o dono do attachment

## MessageAccessPolicy

### Regras do acesso às mensagens

- O usuario acessa apenas as mensagens de seu proprio chat
- Seu chat acessa apenas suas proprias mensagens
- A mensagem (atual e alvo) deve ser do usuário
- O user só pode acessar manipular attachments de suas mensagens

### Ações no acesso em mensagens

- Para atualizar, verificar se o role da mensagem alvo é o mesmo de quem pede a ação
- Verificar se a mensagem alvo é do usuário
- Verificar se o chat pode acessar essa mensagem
- Verificar se quem quer acessar é o dono da mensagem
- Verificar se o usuário pode acessar essa mensagem

## ChatAccessPolicy

### Regras do acesso ao chat

- O usuário acessa seu próprio chat
- O usuário não consegue acessar o chat de outros user

### Ações ao validar o acesso a um chat

- Verificar se quem pede é um usuário
- Verificar se quem pede é o dono do item
