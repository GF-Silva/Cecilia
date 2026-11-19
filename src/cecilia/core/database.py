from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
# TODO (database): put database configs into the .env

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}" # TODO (dabase): Rename to DATABASE_URL

connect_args = {
    "check_same_thread": False
}

engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]