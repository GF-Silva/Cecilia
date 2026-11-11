from cecilia.core.exceptions import BaseError, ValueError, InternalError

class MessagesEmptyError(BaseError):
    def __init__(
        self, 
        messages, 
        error_code: str = "MESSAGES_EMPTY",
        title: str = "Messages Empty",
        status_code: int = 400
    ):
        self.messages = messages
        self.error_code = error_code
        self.title = title
        self.status_code = status_code

        super().__init__(
            message="The messages are empty",
            error_code=error_code,
            values={
                "messages": messages
            },
            status_code=status_code,
            title=title
        )

class InvalidModelIDError(ValueError):
    def __init__(
        self, 
        model_id: str, 
        error_code: str = "INVALID_MODEL_ID",
        title: str = "Invalid model ID",
        status_code: int = 400,
    ):
        self.title = title
        self.status_code = status_code
        self.model_id = model_id
        self.status_code=status_code

        super().__init__(
            title=title,
            status_code=status_code,
            message = f"{model_id} is not a valid model id",
            error_code = error_code,
            values = {
                "model_id": model_id
            }
        )

class SpendingLimitReachedError(BaseError):
    def __init__(
        self, 
        error_code: str = "INTERNAL_SPENDING_LIMIT_REACHED",
        status_code: int = 503,
        title: str = "Internal spending limit reached"
    ):
        super().__init__(
            message = "We are out of AI credits for now, try again later",
            error_code = error_code,
            title=title,
            status_code=status_code
        )

class UnsuportedModelForEndpointError(ValueError):
    def __init__(
        self, 
        model: str, 
        error_code: str = "UNSUPORTED_MODEL_FOR_ENDPOINT",
        title: str = "Unsuported model for endpoint",
        status_code: int = 400
    ):
        self.model = model
        super().__init__(
            message = f'This route does not support the model {model}',
            error_code=error_code,
            values={
                "model": model
            },
            title=title,
            status_code=status_code
        )

class ModelNotSupportAudioError(ValueError):
    def __init__(
        self, 
        model: str, 
        error_code: str = "MODEL_NOT_SUPPORT_AUDIO",
        title: str = "This model does not support audio",
        status_code: int = 400
    ):
        self.model = model
        super().__init__(
            message = f'The model {model} does not support audio input',
            error_code=error_code,
            values={
                "model": model
            },
            title=title,
            status_code=status_code
        )

class ModelNotSupportImageError(ValueError):
    def __init__(
        self, 
        model: str, 
        error_code: str = "MODEL_NOT_SUPPORT_IMAGE",
        title: str = "This model does not support image",
        status_code: int = 400
    ):
        self.model = model
        super().__init__(
            message = f'The model {model} does not support image input',
            error_code=error_code,
            values={
                "model": model
            },
            title=title,
            status_code=status_code
        )

class ShouldSetReasoningForModelError(BaseError):
    def __init__(
        self,
        model: str,
        reasoning_level: str,
        status_code: int = 422,
        error_code: str = 'REASONING_SHOULD_BE_SET_FOR_THIS_MODEL',
        title: str = 'Reasoning should be enabled with this model'
    ):
        self.reasoning_level = reasoning_level
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(
            title=title,
            status_code=status_code,
            message=f'The reasoning should be set for the model {model}',
            error_code=error_code,
            values={
                "model": model,
                "reasoning_effort": reasoning_level
            }
        )