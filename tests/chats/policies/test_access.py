import pytest
from cecilia.policies import ChatAccessPolicy
from cecilia.policies.errors import CannotAccessError

def test_access_accepts_owner():
    chat_access_policy = ChatAccessPolicy()
    chat_access_policy.can_access(
        requester_user_id=10,
        chat_user_id=10
    )

def test_access_refuses_not_owners():
    chat_access_policy = ChatAccessPolicy()

    with pytest.raises(CannotAccessError) as exception:
        chat_access_policy.can_access(
            requester_user_id=10,
            chat_user_id=11
        )

    assert exception.value.status_code == 403
    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'
    assert exception.value.reason_code == 'THIS_CHAT_IS_NOT_YOURS'
