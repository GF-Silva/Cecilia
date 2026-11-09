from dataclasses import asdict
from typing import Sequence

from cecilia.services import MessageService, ReasoningService
from cecilia.integrations import Completions, R2
from cecilia.integrations.hackclub_ai import errors as hcai_errors
from cecilia.integrations.hackclub_ai.types.payload import ReasoningDetails
from cecilia.integrations.hackclub_ai.types.responses import Reasoning
from cecilia.models.message_model import MessageCreate
from cecilia.models.tables import Message as DBMessage
from cecilia.models.reasoning_model import ReasoningCreate
from cecilia.integrations.hackclub_ai.types.messages import (
    Message as HcaiMessage, 
    TextContent, 
    AudioContent,
    Content,
    Audio,
    ImageUrl,
    ImageContent,
    Effort
)
from uuid import UUID
import fastpybase64 as base64

class SendChatMessagesUseCase:
    def __init__(
        self,
        completions_integration: Completions,
        message_service: MessageService,
        r2_integration: R2,
        reasoning_service: ReasoningService
    ):
        self.message_service = message_service
        self.completions_integration = completions_integration
        self.r2_integration = r2_integration
        self.reasoning_service = reasoning_service

    async def __call__(
        self,
        chat_id: UUID, 
        model: str,
        effort: Effort = Effort.NONE
    ):
        db_messages = self.message_service.get_all_by_chat_id(chat_id)

        if not db_messages:
            raise hcai_errors.MessagesEmptyError(db_messages)

        messages = await self._db_to_hcai_messages(db_messages)

        stream = self.completions_integration.create(
            messages=messages,
            model=model,
            effort=effort
        )

        reasonings: list[Reasoning] = []

        async for stream_event in stream:
            if stream_event.event == "finished":
                response = stream_event.full_response

            if stream_event.reasoning:
                reasonings.append(*stream_event.reasoning)
 
            yield stream_event

        db_assistant_message = self.message_service.create(MessageCreate(
            chat_id=chat_id,
            is_user=False,
            text=response
        ))

        db_reasonings = self._handle_reasonings(reasonings, db_assistant_message.id)
        self.reasoning_service.create_list(db_reasonings)

    async def _db_to_hcai_messages(self, db_messages: Sequence[DBMessage]) -> list[HcaiMessage]:
        messages = []

        for db_message in db_messages:
            content: list[Content] = []

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
 
            message = HcaiMessage(
                role="user" if db_message.is_user else "assistant",
                content=content
            ) 

            messages.append(asdict(message))

        return messages
    
    def _handle_reasonings(self, reasonings: list[Reasoning], message_id: int):
        db_reasonings = []

        for reasoning in reasonings:

            last_el = db_reasonings[-1] if db_reasonings else None
            should_merge = last_el is not None and (
                last_el.type == reasoning.type
                and last_el.format == reasoning.format 
                and last_el.encrypted_data == reasoning.encrypted_data
                and last_el.signature == reasoning.signature
                or last_el.signature is None
                and last_el.reasoning_id == reasoning.id
                and last_el.index == reasoning.index
            )

            if not should_merge or not last_el:
                db_reasonings.append(ReasoningCreate(
                    type=reasoning.type,
                    text=reasoning.text,
                    format=reasoning.format,
                    index=reasoning.index,
                    reasoning_id=reasoning.id,
                    signature=reasoning.signature,
                    message_id=message_id,
                    encrypted_data=reasoning.encrypted_data
                ))
                continue
                
            last_el.text = last_el.text + reasoning.text if reasoning.text and last_el.text else last_el.text
            last_el.signature = reasoning.signature
            
        return db_reasonings