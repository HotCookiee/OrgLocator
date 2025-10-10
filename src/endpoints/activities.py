from fastapi import APIRouter, Depends

from services.users import access_token_verification


activity_router = APIRouter()

from uuid import uuid4


from description.organization import HealthDescription as organization_dcp


from repositories.tools import add_object_to_the_database, del_object_to_the_database
from repositories.activities import get_list_organization_by_activity


from models import Activities

from schemas.activity import AddActivity


@activity_router.get(
    "/by-id/{activity_id}/organizations/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_BY_ACTIVITY.value,
    dependencies=[Depends(access_token_verification)]
)
async def get_list_organization_from_activity(activity_id: str):
    org_inf: Activities = await get_list_organization_by_activity(activity_id)
    return {"code": 200, "list_organizations": org_inf}


@activity_router.post(
    "/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)]
)
async def create_activity(organization_schema: AddActivity):
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await add_object_to_the_database(data(AddActivity, organization_schema))


@activity_router.delete(
    "/by-id/{activity_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)]
)
async def delete_activity(activity_id: str):
    return await del_object_to_the_database(AddActivity, activity_id)
