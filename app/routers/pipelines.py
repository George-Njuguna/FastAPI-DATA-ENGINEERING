from ..services.auth import RoleChecker
from ..services.pipelines import FileIngestionService
from ..dependancies.pipelines import get_pipeline_service
from .. import schemas, db

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, status
import logging
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pipelines",
    tags=["Pipeline operations"]
)

allow_engineers = ['engineer', 'admin']

@router.post("/bulk-File-Upload/", response_model = schemas.BulkResponse)
def DemoLoad(
    service: FileIngestionService = Depends(get_pipeline_service),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user = Depends(RoleChecker(allow_engineers))
):
    job = service.create_job_id(
        current_user = current_user,
        triggered_by = current_user.id
    )

    background_tasks.add_task(
        FileIngestionService.demo_bulk_insert,
        job_id = job
    )

    return schemas.BulkResponse(
        status= "Queued",
        job_id = job,
        triggered_by = current_user.email
    )

@router.get("/status/{id}", response_model = schemas.PipeOut)
def GetJobStatus(
    id: UUID,
    service: FileIngestionService = Depends(get_pipeline_service),
    current_user = Depends(RoleChecker(allow_engineers))
):
    return service.get_job_status(id = id)


@router.post("/upload-csv")#response_model = schemas.PipeOut)
async def upload_csv_pipeline(
    file: UploadFile = File(...),  # Instructs FastAPI to expect a file upload parameter
    service: FileIngestionService = Depends(get_pipeline_service),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user = Depends(RoleChecker(allow_engineers))
):
    """
    Secure file endpoint. Accepts a binary .csv file stream, 
    verifies administrative clearance, and dispatches to the parsing engine.
    """
    # 1. Basic format validation check
    if not file.filename.endswith('.csv'):
        return {"error": "Rejected: Only CSV format files are allowed here."}
    
    job = service.create_job_id(
        current_user = current_user,
        triggered_by = current_user.id
    )
        
    # 2. Read the raw stream into byte memory
    file_contents = await file.read()

    background_tasks.add_task(
        FileIngestionService.bulk_insert_csv_stream,
        file_bytes = file_contents,
        triggered_by = current_user.email,
        job_id = job
    )

    
    return {
        "status": "Queued",
        "filename": file.filename,
        "processed_by": current_user.email
    }




