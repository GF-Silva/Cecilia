from typing import Annotated
from fastapi import Depends
from .db_to_openrouter_message_builder import DBToOpenrouterMessageBuilder
from cecilia.integrations import R2IntegrationDep

def get_db_to_openrouter_message_builder(
    r2_integration: R2IntegrationDep
):
    yield DBToOpenrouterMessageBuilder(r2_integration=r2_integration)

DBToOpenrouterMessageBuilderDep = Annotated[DBToOpenrouterMessageBuilder, Depends(get_db_to_openrouter_message_builder)]