from ..services.auth import RoleChecker
from ..services.pipelines import FileIngestionService
from ..dependancies.pipelines import get_pipeline_service
from .. import schemas, db

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, status
import logging

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
    job = service.create_job_id(current_user.email)

    background_tasks.add_task(
        FileIngestionService.demo_bulk_insert,
        triggered_by = current_user.email,
        job_id = job
    )

    return schemas.BulkResponse(
        status= "Queued",
        job_id = job,
        triggered_by = current_user.email
    )



