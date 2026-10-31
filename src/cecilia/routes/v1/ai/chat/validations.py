from .dependencies import ChatServiceDep, MessageServiceDep

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