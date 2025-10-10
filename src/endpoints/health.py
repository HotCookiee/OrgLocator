from fastapi import APIRouter, Depends
from description.health import HealthDescription as health_dcp
from repositories.service import check_the_database_for_life
from services.users import access_token_verification

health_router = APIRouter()


@health_router.get(
    "/liveness",
    openapi_extra={"descriptions_tag": "health"},
    description=health_dcp.HEALTH_LIVENESS.value,
    dependencies=[Depends(access_token_verification)]
)
async def get_status_liveness_service():
    return {"code": "200", "message": "service is alive"}


@health_router.get(
    "/readiness",
    openapi_extra={"descriptions_tag": "health"},
    description=health_dcp.HEALTH_DATABASE.value,
    dependencies=[Depends(access_token_verification)]
)
async def get_status_liveness_database():
    return await check_the_database_for_life()
