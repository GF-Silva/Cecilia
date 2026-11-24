import pytest
from cecilia.policies import AttachmentsAccessPolicy
from cecilia.policies import errors

def test_access_accepts_owner():
    attachments_access_policy = AttachmentsAccessPolicy()
    attachments_access_policy.can_access(requester_user_id=10, attachment_user_id=10)

def test_access_rejects_not_owner():
    attachments_access_policy = AttachmentsAccessPolicy()

    with pytest.raises(errors.CannotAccessError) as exception:
        assert attachments_access_policy.can_access(requester_user_id=10, attachment_user_id=11)

    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'
    assert exception.value.status_code == 403

def test_modify_accepts_owner():
    attachments_access_policy = AttachmentsAccessPolicy()
    attachments_access_policy.can_modify(
        requester_user_id=10, 
        attachment_user_id=10, 
        is_user=True,
        message_is_user=True
    )

def test_modify_rejects_not_owner():
    attachments_access_policy = AttachmentsAccessPolicy()

    with pytest.raises(errors.CannotAccessError) as exception:
        assert attachments_access_policy.can_modify(
            requester_user_id=10, 
            attachment_user_id=11, 
            is_user=True,
            message_is_user=True
        )

    assert exception.value.error_code == 'CANNOT_ACCESS_OTHERS_ITEMS'
    assert exception.value.status_code == 403

def test_modify_rejects_not_users():
    attachments_access_policy = AttachmentsAccessPolicy()
    
    with pytest.raises(errors.CannotAccessError) as exception:
        attachments_access_policy.can_modify(
            requester_user_id=10, 
            attachment_user_id=10, 
            is_user=True,
            message_is_user=False
        )

    assert exception.value.error_code == 'ROLES_MUST_BE_THE_SAME'
    assert exception.value.status_code == 403
