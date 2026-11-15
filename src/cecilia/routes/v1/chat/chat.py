from fastapi import APIRouter

from cecilia.services import ChatServiceDep

from cecilia.models.chat_model import ChatCreate, ChatPublic

router = APIRouter(prefix="/chats", tags=['Chat'])

@router.get('/{user_id}', response_model=list[ChatPublic])
def get_all_by_user_id(user_id: int, chat_service: ChatServiceDep, offset: int = 0, limit: int = 100):
    return chat_service.get_all_by_user_id(user_id=user_id, offset=offset, limit=limit)

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

