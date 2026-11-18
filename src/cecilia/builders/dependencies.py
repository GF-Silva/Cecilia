from typing import Annotated
from fastapi import Depends
from .db_to_openrouter_message_builder import DBToOpenrouterMessageBuilder
from cecilia.integrations import R2IntegrationDep
from cecilia.use_cases.attachments import DeleteAttachmentUseCaseDep

def get_db_to_openrouter_message_builder(
    r2_integration: R2IntegrationDep,
    delete_attachment_use_case: DeleteAttachmentUseCaseDep
):
    yield DBToOpenrouterMessageBuilder(r2_integration=r2_integration, delete_attachment_use_case=delete_attachment_use_case)

DBToOpenrouterMessageBuilderDep = Annotated[DBToOpenrouterMessageBuilder, Depends(get_db_to_openrouter_message_builder)]