import pytest
from cecilia.policies import MessageAccessPolicy, errors
import uuid

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

def test_modify_accepts_owner():
    message_access_policy = MessageAccessPolicy()
    id=uuid.uuid7()

    message_access_policy.can_access(
        requester_user_id=10,
        requester_chat_id=id,
        message_user_id=10,
        message_chat_id=id
    )

def test_modify_rejecs_not_message_owner():
    message_access_policy = MessageAccessPolicy()
    id=uuid.uuid7()

    with pytest.raises(errors.CannotAccessError) as exception:
        message_access_policy.can_modify(
            requester_user_id=20,
            requester_chat_id=id,
            requester_is_user=True,
            message_user_id=10,
            message_chat_id=id,
            message_is_user=True
        )

    assert exception.value.reason_code == 'THIS_MESSAGE_IS_NOT_YOURS'
    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'

def test_modify_rejecs_messages_from_other_chats():
    message_access_policy = MessageAccessPolicy()

    with pytest.raises(errors.CannotAccessError) as exception:
        message_access_policy.can_modify(
            requester_user_id=10,
            requester_chat_id=uuid.uuid7(),
            requester_is_user=True,
            message_user_id=10,
            message_chat_id=uuid.uuid7(),
            message_is_user=True
        )

    assert exception.value.reason_code == 'THIS_CHAT_CANNOT_ACCESS_THIS_MESSAGE'
    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'

def test_modify_rejecs_different_roles():
    message_access_policy = MessageAccessPolicy()
    id=uuid.uuid7()

    with pytest.raises(errors.CannotAccessError) as exception:
        message_access_policy.can_modify(
            requester_user_id=10,
            requester_chat_id=id,
            requester_is_user=True,
            message_user_id=10,
            message_chat_id=id,
            message_is_user=False
        )

    assert exception.value.reason_code == 'THE_MESSAGES_ROLES_ARE_DIFFERENT'
    assert exception.value.error_code == 'ROLES_MUST_BE_THE_SAME'
