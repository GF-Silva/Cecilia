from sqlmodel import select, Session
from cecilia.models.tables import Reasoning
from cecilia.models.reasoning_model import ReasoningCreate
from typing import Sequence

class ReasoningRepository:
    def __init__(
        self,
        session: Session
    ):
        self.session = session

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Reasoning]:
        return self.session.exec(select(Reasoning).offset(offset).limit(limit)).all()

    def show(self, id: int) -> Reasoning | None:
        return self.session.get(Reasoning, id)

    def create(self, reasoning_create: ReasoningCreate):
        reasoning = Reasoning.model_validate(reasoning_create)
        self.session.add(reasoning)
        self.session.commit()
        self.session.refresh(reasoning)

        return reasoning

    def create_list(self, reasonings: list[ReasoningCreate]):
        db_reasonings: list[Reasoning] = [
            Reasoning.model_validate(reasoning)
            for reasoning in reasonings
        ]

        self.session.add_all(db_reasonings)
        self.session.commit()
        
        for i in db_reasonings:
            self.session.refresh(i)

        return db_reasonings