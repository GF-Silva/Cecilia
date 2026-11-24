from cecilia.policies.errors import CannotAccessError, AccessError

class AttachmentsAccessPolicy:
    def can_access(self, requester_user_id: int, attachment_user_id: int):
        if requester_user_id != attachment_user_id:
            raise CannotAccessError(
                resource='Attachments', 
                reason='this is not yours',
                reason_code='THIS_ATTACHMENT_IS_NOT_YOURS',
                error_code=AccessError.THIS_IS_NOT_YOURS
            )
        
        return True

    def can_modify(
        self, 
        requester_user_id: int, 
        attachment_user_id: int, 
        is_user: bool,
        message_is_user: bool
    ):
        if requester_user_id != attachment_user_id:
            raise CannotAccessError(
                resource='Attachments', 
                reason='this is not yours', 
                reason_code='THIS_ATTACHMENT_IS_NOT_YOURS',
                error_code=AccessError.THIS_IS_NOT_YOURS
            )

        if not is_user:
            raise CannotAccessError(
                resource='Attachments', 
                reason='only users can modify attachments',
                reason_code='ONLY_USERS_CAN_MODIFY_ATTACHMENTS',
                error_code=AccessError.ONLY_USERS_CAN_MODIFY
            )

        if is_user != message_is_user:
            raise CannotAccessError(
                resource='Attachments', 
                reason='the message role is different from your role',
                reason_code='THE_MESSAGES_ROLES_MUST_MATCH',
                error_code=AccessError.ROLES_MUST_BE_THE_SAME
            )
        
        return True