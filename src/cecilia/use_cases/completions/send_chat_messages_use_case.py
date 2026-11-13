from uuid import UUID

# Services
from cecilia.services import MessageService

# Integrations
from cecilia.integrations import Completions, R2
from cecilia.integrations.hackclub_ai import errors as hcai_errors
from cecilia.integrations.hackclub_ai.types.messages import (
    Effort
)

# Mappers
from cecilia.builders import DBToOpenrouterMessageBuilder

# Collectors
from cecilia.collectors import CompletionCollector

# Others
from .types import Response

class SendChatMessagesUseCase:
    def __init__(
        self,
        completions_integration: Completions,
        message_service: MessageService,
        completion_collector: CompletionCollector,
        db_to_openrouter_message_builder: DBToOpenrouterMessageBuilder
    ):
        self.message_service = message_service
        self.completions_integration = completions_integration
        self.completion_collector = completion_collector
        self.db_to_openrouter_message_builder = db_to_openrouter_message_builder

    async def __call__(
        self,
        chat_id: UUID, 
        model: str,
        effort: Effort | None = None
    ):
        db_messages = self.message_service.get_all_by_chat_id(chat_id)

        if not db_messages:
            raise hcai_errors.MessagesEmptyError(db_messages)

        messages = [
            await self.db_to_openrouter_message_builder(message)
            for message in db_messages
        ]

        stream = self.completions_integration.create(
            messages=messages,
            model=model,
            effort=effort
        )

        # TODO: This full response field is temporary and should / will be removed
        async for stream_event, full_response in stream:
            self.completion_collector.send_chunk(stream_event)

            yield Response(
                event=stream_event.event,
                chunk=stream_event.chunk,
                reasoning=[
                    reasoning.text
                    for reasoning in stream_event.reasoning
                    if reasoning.text
                ] if stream_event.reasoning else None
            ), ''

        self.completion_collector.save(
            chat_id=chat_id
        )