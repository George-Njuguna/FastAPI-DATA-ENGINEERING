from ..services.auth import RoleChecker
from ..services.pipelines import FileIngestionService
from ..dependancies import pipelines
from .. import schemas, db

from fastapi import FastAPI ,HTTPException, Depends, APIRouter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pipelines",
    tags=["Pipeline operations"]
)

allow_engineers = RoleChecker(['engineer', 'admin'])

#@router.post("/bulk-File-Upload/", response_model = schemas.BulkResponse)
#def BulkLoad(

#)
