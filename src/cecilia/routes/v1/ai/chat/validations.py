from .dependencies import ChatServiceDep, MessageServiceDep
from pydantic import AfterValidator
import re
from typing import Annotated

def validate_chat_id(
    chat_id: int,
    chat_service: ChatServiceDep
):
    chat = chat_service.show(chat_id)

def validate_message_id(
    message_id: int,
    message_service: MessageServiceDep
):
    message = message_service.show(message_id)

def validate_ai_model_name(name: str) -> AIModelName:
    regex = r'^[A-Za-z0-9~._:@+-]+/[A-Za-z0-9~._:@+-]+$'
    
    if not re.match(regex, name):
        raise ValueError('the model should be formated like "nice-provider/model-name"')

    return name

AIModelName = Annotated[str, AfterValidator(validate_ai_model_name)]