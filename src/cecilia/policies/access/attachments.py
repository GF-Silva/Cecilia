from cecilia.policies.errors import CannotAccessError, AccessError

class AttachmentsAccessPolicy:
    def __init__(self):
        pass

    def can_access(self, requester_user_id: int, attachment_user_id: int, is_user: bool):
        if requester_user_id != attachment_user_id:
            raise CannotAccessError(
                resource='Attachments', 
                reason='this is not yours', 
                error_code=AccessError.THIS_IS_NOT_YOURS
            )

        if not is_user:
            raise CannotAccessError(
                resource='Attachments', 
                reason='only users can access',
                error_code=AccessError.ONLY_USERS_CAN_ACCESS
            )
        
        return True

    def can_modify(self, request_user_id: int, attachment_user_id: int):
        return True