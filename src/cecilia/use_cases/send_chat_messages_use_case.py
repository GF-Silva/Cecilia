from dataclasses import asdict

from cecilia.services import MessageService
from cecilia.integrations import Completions, R2
from cecilia.integrations.hackclub_ai import errors as hcai_errors
from cecilia.models.message_model import MessageCreate
from cecilia.integrations.hackclub_ai.types.messages import (
    Message, 
    TextContent, 
    AudioContent,
    Content,
    Audio,
    ImageUrl,
    ImageContent
)
from uuid import UUID
import fastpybase64 as base64

class SendChatMessagesUseCase:
    def __init__(
        self,
        completions_integration: Completions,
        message_service: MessageService,
        r2_integration: R2
    ):
        self.message_service = message_service
        self.completions_integration = completions_integration
        self.r2_integration = r2_integration

    async def __call__(self, chat_id: UUID, model: str):
        db_messages = self.message_service.get_all_by_chat_id(chat_id)

        if not db_messages:
            raise hcai_errors.MessagesEmptyError(db_messages)

        messages: list = []

        for db_message in db_messages:
            content: list = []

            if db_message.text:
                content.append(TextContent(
                    text=db_message.text
                ))

            if db_message.attachments:
                for attachment in db_message.attachments:
                    if attachment.mime_type.startswith("audio/"):
                        file_data = await self.r2_integration.get_file_data(attachment.path)
                        base64_file = base64.b64encode(file_data).decode('utf-8')
                        content.append(AudioContent(
                            input_audio=Audio(
                                format="mp3",
                                data=base64_file
                            )
                        ))

                    if attachment.mime_type.startswith("image/"):
                        presigned_url = await self.r2_integration.generate_presigned_get_url(
                            key=attachment.path
                        )

                        content.append(ImageContent(
                            image_url=ImageUrl(url=presigned_url)
                        ))

            message = Message(
                role="user" if db_message.is_user else "assistant",
                content=content
            )

            messages.append(asdict(message))

        stream = self.completions_integration.create(
            messages=messages,
            model=model
        )

        async for stream_event in stream:
            if stream_event.event == "finished":
                response = stream_event.full_response
                
            yield stream_event

        self.message_service.create(MessageCreate(
            chat_id=chat_id,
            is_user=False,
            text=response
        ))