class HackClubBaseError(Exception):
    def __init__(self, message: str, code: str | None = None, values: dict | None = None):
        super().__init__({
            "message": message,
            "code": code,
            "values": values
        })

class MessagesEmptyError(HackClubBaseError):
    def __init__(self, messages, code: str | None = None):
        self.messages = messages
        self.code = code

        super().__init__(
            message="The messages are empty",
            code=code,
            values={
                "messages": messages
            }
        )

class InvalidModelIDError(HackClubBaseError):
    def __init__(self, model_id: str, code: str | None = None):
        self.model_id = model_id
        self.code=code

        super().__init__(
            message = "Invalid model ID",
            code = code,
            values = {
                "model_id": model_id
            }
        )

class SpendingLimitReachedError(HackClubBaseError):
    def __init__(self, code: str | None = None):
        super().__init__(
            message = "We are out of AI credits for now, try again later",
            code = code
        )

class UnsuportedModelForEndpointError(HackClubBaseError):
    def __init__(self, model: str, code: str | None = None):
        self.model = model
        super().__init__(
            message = f'This route does not support the model {model}',
            code=code,
            values={
                "model": model
            }
        )