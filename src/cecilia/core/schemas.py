from pydantic import BaseModel

class ErrorDetails(BaseModel):
    title: str
    status_code: int
    detail: str
    type: str
    extra_info: dict | None = None