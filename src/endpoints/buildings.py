from fastapi import APIRouter, Depends

from services.users import access_token_verification

building_router = APIRouter()
from uuid import uuid4


from description.organization import HealthDescription as organization_dcp


from repositories.tools import add_object_to_the_database, del_object_to_the_database
from repositories.buildings import get_list_organization_by_building

from models import Buildings


from schemas.building import AddBuilding


@building_router.get(
    "/by-id/{building_id}/organizations",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_BY_BUILDING.value,
    dependencies=[Depends(access_token_verification)]
)
async def get_list_organization_from_building(building_id: str):
    org_inf: Buildings = await get_list_organization_by_building(building_id)
    return {"code": 200, "list_organizations": org_inf}


@building_router.post(
    "/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.BYL_CREATE.value,
    dependencies=[Depends(access_token_verification)]
)
async def create_build(build_schema: AddBuilding):
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await add_object_to_the_database(data(Buildings, build_schema))


@building_router.delete(
    "/by-id/{building_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)]
)
async def delete_build(building_id: str):
    return await del_object_to_the_database(Buildings, building_id)
