from cecilia.core.exceptions import BaseError, ValueError

class MessagesEmptyError(BaseError):
    def __init__(self, messages, error_code: str = "MESSAGES_EMPTY"):
        self.messages = messages
        self.error_code = error_code

        super().__init__(
            message="The messages are empty",
            error_code=error_code,
            values={
                "messages": messages
            }
        )

class InvalidModelIDError(ValueError):
    def __init__(self, model_id: str, error_code: str = "INVALID_MODEL_ID"):
        self.model_id = model_id
        self.error_code=error_code

        super().__init__(
            message = f"{model_id} is not a valid model id",
            error_code = error_code,
            values = {
                "model_id": model_id
            }
        )

class SpendingLimitReachedError(BaseError):
    def __init__(self, error_code: str = "INTERNAL_SPENDING_LIMIT_REACHED"):
        super().__init__(
            message = "We are out of AI credits for now, try again later",
            error_code = error_code
        )

class UnsuportedModelForEndpointError(ValueError):
    def __init__(self, model: str, error_code: str = "UNSUPORTED_MODEL_FOR_ENDPOINT"):
        self.model = model
        super().__init__(
            message = f'This route does not support the model {model}',
            error_code=error_code,
            values={
                "model": model
            }
        )