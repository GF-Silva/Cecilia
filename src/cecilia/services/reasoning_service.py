from cecilia.models.reasoning_model import ReasoningCreate
from cecilia.repositories import ReasoningRepository
from cecilia.core.exceptions import NotFoundError

class ReasoningService:
    def __init__(
        self,
        reasoning_repository: ReasoningRepository
    ):
        self.reasoning_repository = reasoning_repository

    def index(self, offset: int = 0, limit: int = 100):
        return self.reasoning_repository.index(offset, limit)

    def show(self, id: int):
        db_reasoning = self.reasoning_repository.show(id)

        if not db_reasoning:
            raise NotFoundError(
                resource='Reasoning',
                item=id
            )

        return db_reasoning

    def create(self, reasoning_create: ReasoningCreate):
        db_reasoning = self.reasoning_repository.create(reasoning_create)

        return db_reasoning
    
    def create_list(self, reasonings: list[ReasoningCreate]):
        db_reasonings = self.reasoning_repository.create_list(reasonings)
        return db_reasonings