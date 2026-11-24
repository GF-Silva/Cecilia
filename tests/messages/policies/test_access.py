import pytest
from cecilia.policies import MessageAccessPolicy, errors
import uuid

# Regras do acesso às mensagens
# O usuario acessa apenas as mensagens de seu proprio chat
# Seu chat acessa apenas suas proprias mensagens
# A mensagem (atual e alvo) deve ser do usuário
# O user só pode acessar manipular attachments de suas mensagens

# Ações no acesso em mensagens
# Para atualizar, verificar se o role da mensagem alvo é o mesmo de quem pede a ação
# Verificar se a mensagem alvo é do usuário
# Verificar se o chat pode acessar essa mensagem
# Verificar se quem quer acessar é o dono da mensagem
# Verificar se o usuário pode acessar essa mensagem

def test_access_accepts_owner():
    message_access_policy = MessageAccessPolicy()
    id=uuid.uuid7()

    message_access_policy.can_access(
        requester_user_id=10,
        requester_chat_id=id,
        message_user_id=10,
        message_chat_id=id
    )

def test_access_rejecs_not_message_owner():
    message_access_policy = MessageAccessPolicy()
    id=uuid.uuid7()

    with pytest.raises(errors.CannotAccessError) as exception:
        message_access_policy.can_access(
            requester_user_id=20,
            requester_chat_id=id,
            message_user_id=10,
            message_chat_id=id
        )

    assert exception.value.reason_code == 'THIS_MESSAGE_IS_NOT_YOURS'
    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'

def test_access_rejecs_messages_from_other_chats():
    message_access_policy = MessageAccessPolicy()

    with pytest.raises(errors.CannotAccessError) as exception:
        message_access_policy.can_access(
            requester_user_id=10,
            requester_chat_id=uuid.uuid7(),
            message_user_id=10,
            message_chat_id=uuid.uuid7()
        )

    assert exception.value.reason_code == 'THIS_CHAT_CANNOT_ACCESS_THIS_MESSAGE'
    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'
