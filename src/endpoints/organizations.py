import json
from fastapi import APIRouter, Depends
from src.description.organization import HealthDescription as organization_dcp
from src.description.selection_by_filter import (
    HealthDescription as selection_by_filter_dcp,
)
from src.repositories.tools import DataBase, Redis as RedisDB

from src.repositories.organizations import GetInfoFromOrganization
from src.models import Organizations
from src.schemas.organization import AddOrganization, SelectOrganization
from src.services.organizations import CoordinateScope
from src.services.users import access_token_verification
from src.services.tools import get_object_from_db_or_cache


organization_router = APIRouter()


@organization_router.get(
    "/by-id/{organization_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_GET_BY_ID.value,
    dependencies=[Depends(access_token_verification)],
)
async def get_info_organization(organization_id: str):
    obj = await get_object_from_db_or_cache(
        key=f"organizations_id_{organization_id}",
        object_model=Organizations,
        object_schema=SelectOrganization,
    )
    return {"code": 200, "organization_info": obj}


@organization_router.post(
    "/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def create_organization(organization_schema: AddOrganization):
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await DataBase.add_object_to_the_database(
        data(Organizations, organization_schema)
    )


@organization_router.delete(
    "/by-id/{organization_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def delete_organization(organization_id: str):
    return await DataBase.del_object_to_the_database(Organizations, organization_id)


@organization_router.get(
    "/search/geo",
    openapi_extra={"descriptions_tag": "selection_by_filter"},
    description=selection_by_filter_dcp.ORG_SEARCH_GEO.value,
    dependencies=[Depends(access_token_verification)],
)
async def get_organization_using_a_filter(
    latitude: float,
    longitude: float,
    radius: int | None = None,
    min_lat: float | None = None,
    max_lat: float | None = None,
    min_lon: float | None = None,
    max_lon: float | None = None,
):

    return await CoordinateScope.search_organizations_by_geo(
        latitude, longitude, radius, min_lat, max_lat, min_lon, max_lon
    )


@organization_router.get(
    "/by-name/{name}",
    openapi_extra={"descriptions_tag": "selection_by_filter"},
    description=selection_by_filter_dcp.ORG_SEARCH_NAME.value,
    dependencies=[Depends(access_token_verification)],
)
async def get_organization_by_name(name_organization: str):
    return await GetInfoFromOrganization.get_info_organization_by_name(
        name_organization
    )
