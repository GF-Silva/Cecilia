from typing import Annotated
from fastapi import Depends
from .db_to_openrouter_message_builder import DBToOpenrouterMessageBuilder
from cecilia.integrations import R2IntegrationDep
from cecilia.use_cases.attachments import AttachmentDeleteUseCaseDep

def get_db_to_openrouter_message_builder(
    r2_integration: R2IntegrationDep,
    attachment_delete_use_case: AttachmentDeleteUseCaseDep
):
    yield DBToOpenrouterMessageBuilder(
        r2_integration=r2_integration, 
        attachment_delete_use_case=attachment_delete_use_case)

DBToOpenrouterMessageBuilderDep = Annotated[DBToOpenrouterMessageBuilder, Depends(get_db_to_openrouter_message_builder)]