from cecilia.policies.errors import CannotAccessError, AccessError

class ChatAccessPolicy:
    def can_access(
        self,
        requester_user_id: int,
        chat_user_id: int
    ):
        if requester_user_id != chat_user_id:
            raise CannotAccessError(
                resource='Chats', 
                reason='this is not yours',
                reason_code='THIS_CHAT_IS_NOT_YOURS',
                error_code=AccessError.THIS_IS_NOT_YOURS
            )

        return True