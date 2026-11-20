from cecilia.core import exceptions
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentUpdate
import pytest

@pytest.mark.parametrize(
    'is_user, should_work',
    [
        (False, False),
        (True, True)
    ]
)
def test_validate_message(mocker, message, is_user, should_work):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    gen_message = message(is_user=is_user)

    if should_work:
        service.validate_message_role(gen_message)
    else:
        with pytest.raises(exceptions.RuleError):
            service.validate_message_role(gen_message)

def test_show_success(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    result = attachment_service.show(message_id=gen_attachment.message_id, id=gen_attachment.id)
    assert result == gen_attachment

def test_show_returns_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.show(id=2, message_id=1)

@pytest.mark.parametrize(
    'is_user, should_work',
    [
        (True, True),
        (False, False)
    ]
)
def test_create(create_attachment, attachment_service, message, is_user, should_work):
    if should_work:
        attachment_service.create(attachment=create_attachment(), message=message(is_user=is_user))
    else:
        with pytest.raises(exceptions.RuleError):
            attachment_service.create(attachment=create_attachment(), message=message(is_user=is_user))

@pytest.mark.parametrize(
    'is_user, should_work',
    [
        (True, True),
        (False, False)
    ]
)
def test_create_list(create_attachment, attachment_service, message, is_user, should_work):
    attachments = [
        create_attachment(),
        create_attachment(),
        create_attachment()
    ]

    if should_work:
        attachment_service.create_list(attachments=attachments, message=message(is_user=is_user))
    else:
        with pytest.raises(exceptions.RuleError):
            attachment_service.create_list(attachments=attachments, message=message(is_user=is_user))

def test_delete_success(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    attachment_service.delete(id=1, message_id=1)

def test_delete_error_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.delete(id=2, message_id=1)

@pytest.mark.parametrize(
    'id, message_id, update_fields, should_work',
    [
        (1, 2, AttachmentUpdate(mime_type='test/test', message_id=10, is_valid=True), True),
        (10, 2, AttachmentUpdate(mime_type='test/test', message_id=10, is_valid=True), False)
    ]
)
def test_update(attachment_service, attachment, id, message_id, update_fields, should_work):
    gen_attachment = attachment(id=1, message_id=2)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment

    if should_work:
        updated_attachment = attachment_service.update(id=id, message_id=message_id, attachment_update=update_fields)
        assert updated_attachment.model_dump(include=update_fields.model_dump(exclude_unset=True)) == update_fields.model_dump(exclude_unset=True)
    else:
        with pytest.raises(exceptions.NotFoundError):
            attachment_service.update(id=id, message_id=message_id, attachment_update=update_fields)