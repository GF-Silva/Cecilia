# Core elements
from cecilia.core.settings import settings
from cecilia.core.exceptions import InternalError

# Services
from cecilia.services import ChatServiceDep, MessageServiceDep, AttachmentServiceDep, ReasoningServiceDep

# Integrations
from cecilia.integrations import HCAICompletionIntegrationDep, R2IntegrationDep

# Use cases
from cecilia.use_cases import CreateAttachmentsUseCaseDep, SendChatMessagesUseCaseDep

# Collectors
from cecilia.collectors import CompletionCollector

# Builders
from cecilia.builders import DBToOpenrouterMessageBuilder

# Adapters
from cecilia.adapters import FFProbeAdapterDep

# Validators
from cecilia.validators import AudioValidatorDep, ImageValidatorDep

# Python libs
from fastapi import Depends
from typing import Annotated

# TODO: Separar as dependencies em diversos arquivos de alto nivel nas suas respectivas classes