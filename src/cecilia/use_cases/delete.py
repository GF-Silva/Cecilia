from cecilia.integrations import R2 
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentUpdate

class DeleteAttachmentUseCase:
    def __init__(
        self,
        r2_integration: R2,
        attachments_service: AttachmentService
    ):
        self.r2_integration = r2_integration
        self.attachments_service = attachments_service

    async def __call__(self, attachment_id: int, message_id: int):
        # O attachments.invalidate_file invalida o arquivo internamente no attachments,
        # ent ele tenta deletar? Aq ele pode ou deletar ou mandar pra um background worker fazer isso
        # talvez um worker na r2 e outro no database. Ai o codigo apenas alterna um estado, ent n dmr mt
        # tempo deletando um arquivo. Assim da pra integrar com outras coisas pra comecar a processar
        # os arquivos em background, ex: na hr de criar ele valida em background, e se alguma rota acessar
        # enquanto ele n esta validado, o codigo tenta, se der erro ele remove o arquivo

        # Definir o estado do arquivo no database como invalido
        # Aplicar o worker da R2 para deletar arquivos invalidados
        # Tirar a validacao de arquivos do codigo e passar para um worker

        attachment = self.attachments_service.update(
            id=attachment_id,
            message_id=message_id,
            attachment_update=AttachmentUpdate(is_valid=False)
        )

        await self.r2_integration.delete_file(attachment.path)