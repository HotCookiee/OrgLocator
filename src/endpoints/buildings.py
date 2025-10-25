from fastapi import APIRouter, Depends
from src.services.users import access_token_verification
from src.description.organization import HealthDescription as organization_dcp
from src.repositories.tools import DataBase
from src.models import Buildings
from src.schemas.building import AddBuilding, SelectBuilding



building_router = APIRouter()


@building_router.get(
    "/by-id/{building_id}/organizations",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_BY_BUILDING.value,
    dependencies=[Depends(access_token_verification)],
)
async def get_list_organization_from_building(building_id: str):
    org_inf: Buildings = await DataBase.get_objects_from_database_by_id_or_name(
        Buildings,SelectBuilding, building_id, field="id"
    )
    # org_inf: Buildings = await get_list_organization_by_building(building_id)
    return {"code": 200, "list_organizations": org_inf}


@building_router.post(
    "/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.BYL_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def create_build(build_schema: AddBuilding):
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await DataBase.add_object_to_the_database(data(Buildings, build_schema))


@building_router.delete(
    "/by-id/{building_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def delete_build(building_id: str):
    return await DataBase.del_object_to_the_database(Buildings, building_id)
