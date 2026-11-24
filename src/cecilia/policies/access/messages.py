from uuid import UUID
from cecilia.policies.errors import CannotAccessError, AccessError

class MessageAccessPolicy:
    def can_access(
        self,
        requester_user_id: int,
        requester_chat_id: UUID, 
        message_user_id: int,
        message_chat_id: UUID
    ):
        if requester_user_id != message_user_id:
            raise CannotAccessError(
                resource='Messages', 
                error_code=AccessError.THIS_IS_NOT_YOURS,
                reason_code='THIS_MESSAGE_IS_NOT_YOURS'
            )

        if requester_chat_id != message_chat_id:
            raise CannotAccessError(
                resource='Messages', 
                error_code=AccessError.THIS_IS_NOT_YOURS,
                reason_code='THIS_CHAT_CANNOT_ACCESS_THIS_MESSAGE'
            )
    
        return True

    def can_modify(
        self,
        requester_user_id: int,
        requester_chat_id: UUID, 
        requester_is_user: bool,
        message_user_id: int,
        message_chat_id: UUID,
        message_is_user: bool
    ):
        if requester_user_id != message_user_id:
            raise CannotAccessError(
                resource='Messages', 
                error_code=AccessError.THIS_IS_NOT_YOURS,
                reason_code='THIS_MESSAGE_IS_NOT_YOURS'
            )

        if requester_chat_id != message_chat_id:
            raise CannotAccessError(
                resource='Messages', 
                error_code=AccessError.THIS_IS_NOT_YOURS,
                reason_code='THIS_CHAT_CANNOT_ACCESS_THIS_MESSAGE'
            )

        if requester_is_user != message_is_user:
            raise CannotAccessError(
                resource='Messages', 
                error_code=AccessError.ROLES_MUST_BE_THE_SAME,
                reason_code='THE_MESSAGES_ROLES_ARE_DIFFERENT'
            )

        return True