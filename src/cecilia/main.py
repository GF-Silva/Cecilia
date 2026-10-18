from fastapi import FastAPI, Depends, HTTPException, Query
from scalar_fastapi import add_scalar_reference
from .routes.api import api_router

from cecilia.services.attachment_service import AttachmentService, AttachmentPublic, AttachmentCreate, AttachmentRepository
from cecilia.core.database import create_db_and_tables, SessionDep

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
