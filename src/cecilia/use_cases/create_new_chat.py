from cecilia.services import ChatService, MessageService, AttachmentService
from cecilia.models.chat_model import ChatCreate
from cecilia.models.message_model import MessageCreate
from cecilia.models.attachment_model import AttachmentCreate
from cecilia.integrations.open_router import Chat
from cecilia.integrations.open_router.types import Contents

class CreateNewChat:
    def __init__(
        self,
        chat_service: ChatService,
        message_service: MessageService,
        attachment_service: AttachmentService,
        open_router_chat: Chat
    ):
        self.chat_service = chat_service
        self.message_service = message_service
        self.attachment_service = attachment_service
        self.open_router_chat = open_router_chat

    async def execute(
        self,
        user_id: int,
        ai_model: str,
        contents: Contents
    ):
        # Cria o novo chat
        chat_create = ChatCreate(
            user_id=user_id
        )
        db_chat = self.chat_service.create(chat_create)

        # Cria a nova mensagem referenciando esse chat novo
        message_create = MessageCreate(
            role="user",
            chat_id=db_chat.id,
            content=contents.prompt
        )
        db_message = self.message_service.create(message_create)

        # Cria os attachments dessa mensagem
        db_attachments = []
    
        if contents.audios:
            for audio in contents.audios:
                db_attachment = self.attachment_service.create(AttachmentCreate(
                    type=audio.format,
                    data=audio.data,
                    message_id=db_message.id
                ))

                db_attachments.append(db_attachment)

        # Enviar o contents para a IA
        ai_response_stream = self.open_router_chat.send(
            model=ai_model,
            contents=contents
        )

        ai_response = ""
        async for chunk in ai_response_stream:
            if chunk.event == "finished":
                ai_response = chunk.raw_data

            yield chunk

        # Salvar esses contents gerados pela IA no database
        self.message_service.create(MessageCreate(
            role="assistant",
            chat_id=db_chat.id,
            content=ai_response
        ))