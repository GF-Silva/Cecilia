from cecilia.core.exceptions import BaseError
from typing import Any
from enum import StrEnum

class AccessError(StrEnum):
    CANNOT_ACCESS = 'CANNOT_ACCESS'
    THIS_IS_NOT_YOURS = 'CANNOT_ACCESS_OTHERS_ITEMS'
    ONLY_USERS_CAN_MODIFY = 'ONLY_USERS_CAN_MODIFY'
    ROLES_MUST_BE_THE_SAME = 'ROLES_MUST_BE_THE_SAME'

class CannotAccessError(BaseError):
    def __init__(
        self,
        resource: str,
        status_code: int = 403,
        reason: str | None = None, 
        error_code: AccessError = AccessError.CANNOT_ACCESS,
        values: dict[str, Any] | None = None
    ):
        self.resource=resource
        self.status_code=status_code
        self.error_code=error_code
        self.values=values

        super().__init__(
            title=f'Cannot access {resource}',
            status_code=status_code,
            message=f"You cannot the acces the resource {resource} because {reason}",
            error_code=error_code,
            values=values
        )
