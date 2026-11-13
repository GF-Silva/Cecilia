import mimetypes

from cecilia.models.tables import (
    Reasoning, 
    Attachment as DBAttachment,
    Message as DBMessage
)
from cecilia.integrations.hackclub_ai.types.messages import (
    Message as HcaiMessage, 
    TextContent, 
    AudioContent,
    Content,
    Audio,
    ImageUrl,
    ImageContent,
    TextReasoning,
    EncryptedReasoning,
    SummaryReasoning
)
from cecilia.integrations.cloudflare.r2 import R2
import fastpybase64 as base64

class DBToOpenrouterMessageBuilder:
    def __init__(
        self,
        r2_integration: R2
    ):
        self.r2_integration = r2_integration

    async def __call__(self, db_message: DBMessage):
        reasonings = [
            self._build_reasoning(reasoning)
            for reasoning in db_message.reasonings
            if reasoning.type in ['encrypted', 'summary', 'text']
        ] if db_message.reasonings else None

        message = HcaiMessage(
            role="user" if db_message.is_user else "assistant",
            content=await self._build_content(db_message),
            reasoning_details=reasonings
        ) 

        return message

    async def _build_content(self, db_message: DBMessage):
        content: list[Content] = []

        if db_message.text:
            content.append(TextContent(
                text=db_message.text
            ))

        attachments = [
            attachment
            for db_attachment in db_message.attachments
            if (attachment := await self._build_attachment(db_attachment)) is not None
        ] if db_message.attachments else None
        if attachments: content += attachments

        return content

    async def _build_attachment(self, db_attachment: DBAttachment) -> Content | None:
        file_extension = mimetypes.guess_extension(db_attachment.mime_type)

        if not file_extension: print("mime"); return

        if db_attachment.mime_type.startswith("audio/"):
            try:
                file_data = await self.r2_integration.get_file_data(db_attachment.path)
            except FileNotFoundError:
                # TODO: Aplicar a regra de negocio de invalidar o arquivo
                return

            base64_file = base64.b64encode(file_data).decode('utf-8')

            return AudioContent(
                input_audio=Audio(
                    format=file_extension.lstrip('.'),
                    data=base64_file
                )
            )

        if db_attachment.mime_type.startswith("image/"):
            try:
                presigned_url = await self.r2_integration.generate_presigned_get_url(
                    path=db_attachment.path
                )
            except FileNotFoundError:
                # TODO: Aplicar a regra de negocio de invalidar o arquivo
                return

            if not presigned_url: return # TODO: Must invalidate the file into db

            return ImageContent(
                image_url=ImageUrl(url=presigned_url)
            )

    def _build_reasoning(self, reasoning: Reasoning):
        reasoning_data = {
            "format": reasoning.format,
            "id": reasoning.reasoning_id,
            "index": reasoning.index
        }

        if reasoning.type == 'text':
            return TextReasoning(**reasoning_data, text=reasoning.text, signature=reasoning.signature)
        elif reasoning.type == 'summary':
            return SummaryReasoning(**reasoning_data, summary=reasoning.text or '')
        else:
            return EncryptedReasoning(**reasoning_data, data=reasoning.encrypted_data or '')