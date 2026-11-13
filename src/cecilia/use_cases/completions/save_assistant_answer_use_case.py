from cecilia.services import MessageService, ReasoningService
from cecilia.models.reasoning_model import ReasoningCreate
from cecilia.models.message_model import MessageCreate
from cecilia.integrations.hackclub_ai.types.responses import Reasoning as HcaiReasoning, SSEResponse

import uuid

class SaveAssistantAnswerUseCase:
    def __init__(
        self,
        message_service: MessageService,
        reasoning_service: ReasoningService
    ):
        self.message_service = message_service
        self.reasoning_service = reasoning_service

    def __call__(
        self, 
        assistant_answer: list[SSEResponse],
        chat_id: uuid.UUID
    ):
        reasonings = []
        response = ""
        for chunk in assistant_answer:
            if chunk.chunk:
                response += chunk.chunk

            if chunk.reasoning:
                reasonings.append(*chunk.reasoning)

        db_assistant_message = self.message_service.create(MessageCreate(
            chat_id=chat_id,
            is_user=False,
            text=response
        ))

        db_reasonings = self._hcai_to_db_reasonings(reasonings, db_assistant_message.id)
        self.reasoning_service.create_list(db_reasonings)

        return db_assistant_message

    def _hcai_to_db_reasonings(self, reasonings: list[HcaiReasoning], message_id: int) -> list[ReasoningCreate]:
        db_reasonings_create: list[ReasoningCreate] = []

        for reasoning in reasonings:
            last_el = db_reasonings_create[-1] if db_reasonings_create else None
            should_merge = last_el is not None and (
                last_el.type == reasoning.type
                and last_el.format == reasoning.format 
                and last_el.reasoning_id == reasoning.id
                and last_el.index == reasoning.index
            )

            if not should_merge or not last_el:
                db_reasonings_create.append(ReasoningCreate(
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
            last_el.signature = reasoning.signature if not last_el.signature else last_el.signature
            last_el.encrypted_data = reasoning.encrypted_data if not last_el.encrypted_data else last_el.encrypted_data
            
        return db_reasonings_create