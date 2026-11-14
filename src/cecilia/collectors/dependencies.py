from .completion_collector import CompletionCollector
from cecilia.services import MessageServiceDep, ReasoningServiceDep
from typing import Annotated
from fastapi import Depends

def get_completion_collector(
    message_service: MessageServiceDep,
    reasoning_service: ReasoningServiceDep
):
    return CompletionCollector(message_service=message_service, reasoning_service=reasoning_service)

CompletionCollectorDep = Annotated[CompletionCollector, Depends(get_completion_collector)]
