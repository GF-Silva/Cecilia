from fastapi import FastAPI, Depends, HTTPException, Query
from scalar_fastapi import add_scalar_reference
from .routes.api import api_router

from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

from cecilia.services.attachment_service import AttachmentService, AttachmentPublic, AttachmentCreate, AttachmentRepository

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": False
}

engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI(title="Cecília API")

add_scalar_reference(app)
app.include_router(api_router, prefix='/api')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_attachment_repository(session: SessionDep) -> AttachmentRepository:
    return AttachmentRepository(session)

def get_attachment_service(repository: AttachmentRepository = Depends(get_attachment_repository)) -> AttachmentService:
    return AttachmentService(repository)

@app.get("/attachments", response_model=list[AttachmentPublic])
def get_attachments(
    service: AttachmentService = Depends(get_attachment_service),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return service.index(offset, limit)

@app.post("/attachments", response_model=AttachmentPublic)
def create_attachment(
    attachment: AttachmentCreate,
    service: AttachmentService = Depends(get_attachment_service)
):
    return service.create(attachment)

@app.get("/attachments/{id}", response_model=AttachmentPublic)
def show_attachment(
    id: int,
    service: AttachmentService = Depends(get_attachment_service)
):
    return service.show(id)

@app.delete('/attachments/{id}')
def delete_attachment(id: int, service: AttachmentService = Depends(get_attachment_service)):
    return service.delete(id)
