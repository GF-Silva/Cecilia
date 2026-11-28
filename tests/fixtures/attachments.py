from datetime import datetime, UTC
import pytest
import uuid
from dataclasses import dataclass
from typing import Any

from tests.fakes.repositories import FakeAttachmentRepository
from cecilia.services import AttachmentService
from cecilia.models import Attachment, Message, Chat, AttachmentCreate
from cecilia.use_cases import AttachmentCreateUseCase
from cecilia.extractors import FileMetadata

@pytest.fixture
def fake_attachment_repo():
    return FakeAttachmentRepository()

@pytest.fixture
def attachment_service(fake_attachment_repo, mocker): # TODO: Substituir esse repo por um veridico
    mock_message_repo = mocker.MagicMock()
    return AttachmentService(attachment_repository=fake_attachment_repo, message_repository=mock_message_repo)

@pytest.fixture
def attachment_create():
    def _factory(
        mime_type: str = 'audio/mpeg',
        message_id: int = 1,
        size: int | None = None,
        filename: uuid.UUID | None = None,
        public_filename: str | None = None,
        is_valid: bool | None = None
    ):
        return AttachmentCreate(
            mime_type=mime_type, 
            message_id=message_id, 
            size=size, 
            filename=filename if filename is not None else uuid.uuid7(),
            public_filename=public_filename,
            is_valid=is_valid
        )
    
    return _factory

@pytest.fixture
def attachment(attachment_create):
    def _factory(
        created_at: datetime | None = None,
        id: int = 1,
        **kwargs
    ):
        return Attachment(
            **attachment_create(**kwargs).model_dump(),
            created_at=created_at if created_at is not None else datetime.now(UTC),
            id=id
        )
    
    return _factory

@pytest.fixture
def attachment_invalid():
    def _factory(db_attachment: Attachment):
        return Attachment.model_validate({
            **db_attachment.model_dump(),
            "is_valid": False
        })

    return _factory

@dataclass
class CreateUseCaseFixture:
    create_use_case: AttachmentCreateUseCase
    gen_files: list
    create_facade: Any
    file_metada_extractor: Any
    validation_policy_dispatcher: Any
    service: Any
    r2_integration: Any
    gen_chat: Chat
    gen_message: Message
    user_id: int

@pytest.fixture
def attachment_create_use_case(mocker, chat, message, attachment, file):
    def _factory(
        user_id: int = 1,
        gen_chat: Chat | None = None,
        gen_message: Message | None = None,
        gen_files: list | None = None
    ):
        gen_chat=gen_chat if gen_chat else chat()
        gen_message=gen_message if gen_message else message()
        gen_files = gen_files if gen_files else [
            next(file(
                mime_type='image/png',
                type='png'
            ))
        ]

        mock_create_facade = mocker.MagicMock()
        mock_file_metada_extractor = mocker.MagicMock()
        mock_validation_policy_dispatcher = mocker.MagicMock()
        mock_service = mocker.MagicMock()
        mock_r2_integration = mocker.AsyncMock()

        mock_file_metada_extractor.side_effect = [
            FileMetadata(
                mime_type=gen_file.mime_type,
                size=gen_file.size
            ) for gen_file in gen_files
        ]

        mock_service.create_list.return_value = [
            attachment(
                id=id,
                mime_type=file.mime_type, 
                size=file.size, 
                message_id=gen_message.id, 
                public_filename=file.public_filename, 
                is_valid=True
            ) for id, file in enumerate(gen_files, 1)
        ]

        create_use_case = AttachmentCreateUseCase(
            create_facade=mock_create_facade,
            file_metada_extractor=mock_file_metada_extractor,
            validation_policy_dispatcher=mock_validation_policy_dispatcher,
            service=mock_service,
            r2_integration=mock_r2_integration
        )

        return CreateUseCaseFixture(
            create_use_case=create_use_case,
            gen_files=gen_files,
            create_facade=mock_create_facade,
            file_metada_extractor=mock_file_metada_extractor,
            validation_policy_dispatcher=mock_validation_policy_dispatcher,
            service=mock_service,
            r2_integration=mock_r2_integration,
            gen_chat=gen_chat,
            gen_message=gen_message,
            user_id=user_id
        )
    
    return _factory
