from cecilia.services import MessageService, ReasoningService
from cecilia.models.reasoning_model import ReasoningCreate
from cecilia.models.message_model import MessageCreate
from cecilia.integrations.hackclub_ai.types.responses import (
    Reasoning as HcaiReasoning, 
    SSEResponse,
    Response
)

import uuid

class CompletionCollector:
    def __init__(
        self,
        message_service: MessageService,
        reasoning_service: ReasoningService
    ):
        self.message_service = message_service
        self.reasoning_service = reasoning_service
        self.response: Response = Response()

    def send_chunk(self, chunk: SSEResponse):
        if chunk.chunk:
            if not self.response.text:
                self.response.text = chunk.chunk
            else:
                self.response.text += chunk.chunk

        if chunk.reasoning:
            for reasoning in chunk.reasoning: self._handle_reasoning(reasoning)

    def _handle_reasoning(self, reasoning: HcaiReasoning):
        last_el = self.response.reasonings[-1] if self.response.reasonings else None

        should_merge = last_el is not None and (
            last_el.type == reasoning.type
            and last_el.format == reasoning.format 
            and last_el.id == reasoning.id
            and last_el.index == reasoning.index
        )

        if not should_merge or not last_el:
            hcai_reasoning = HcaiReasoning(
                type=reasoning.type,
                text=reasoning.text,
                format=reasoning.format,
                index=reasoning.index,
                id=reasoning.id,
                signature=reasoning.signature,
                encrypted_data=reasoning.encrypted_data
            )

            if self.response.reasonings is None:
                self.response.reasonings = []

            self.response.reasonings.append(hcai_reasoning)
            return
            
        last_el.text = last_el.text + reasoning.text if reasoning.text and last_el.text else last_el.text
        last_el.signature = reasoning.signature if not last_el.signature else last_el.signature
        last_el.encrypted_data = reasoning.encrypted_data if not last_el.encrypted_data else last_el.encrypted_data

    def save(
        self,
        chat_id: uuid.UUID
    ):
        db_message_create = MessageCreate(
            is_user=False,
            chat_id=chat_id,
            text=self.response.text
        )

        db_message_assistant = self.message_service.create(db_message_create)

        db_reasonings_create = [
            ReasoningCreate(
                text=reasoning.text,
                message_id=db_message_assistant.id,
                type=reasoning.type,
                format=reasoning.format,
                encrypted_data=reasoning.encrypted_data,
                reasoning_id=reasoning.id,
                signature=reasoning.signature,
                index=reasoning.index
            )
            for reasoning in self.response.reasonings
        ] if self.response.reasonings else None

        if db_reasonings_create:
            self.reasoning_service.create_list(db_reasonings_create)