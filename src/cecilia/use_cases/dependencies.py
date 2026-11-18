from fastapi import Depends
from typing import Annotated

from cecilia.services import MessageServiceDep
from cecilia.integrations import HCAICompletionIntegrationDep
from cecilia.collectors import CompletionCollectorDep
from cecilia.builders import DBToOpenrouterMessageBuilderDep

from .completions.send_chat_messages_use_case import SendChatMessagesUseCase

def get_send_chat_messages_use_case(
    completions_integration: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    completion_collector: CompletionCollectorDep,
    db_to_openrouter_message_builder: DBToOpenrouterMessageBuilderDep
):
    return SendChatMessagesUseCase(
        completions_integration=completions_integration,
        message_service=message_service,
        db_to_openrouter_message_builder=db_to_openrouter_message_builder,
        completion_collector=completion_collector
    )

SendChatMessagesUseCaseDep = Annotated[SendChatMessagesUseCase, Depends(get_send_chat_messages_use_case)]