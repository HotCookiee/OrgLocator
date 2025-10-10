from fastapi import APIRouter, Depends
from description.organization import HealthDescription as organization_dcp
from description.selection_by_filter import HealthDescription as selection_by_filter_dcp
from repositories.tools import (
    get_objects_from_database,
    add_object_to_the_database,
    del_object_to_the_database,
)
from repositories.organizations import GetInfoFromOrganization
from models import Organizations
from schemas.organization import AddOrganization
from services.organizations import CoordinateScope
from services.users import access_token_verification


organization_router = APIRouter()


@organization_router.get(
    "/by-id/{organization_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_GET_BY_ID.value,
    dependencies=[Depends(access_token_verification)],
)
async def get_info_organization(organization_id: str):
    org_inf: Organizations = await get_objects_from_database(
        Organizations, organization_id
    )
    return org_inf


@organization_router.post(
    "/",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ORG_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def create_organization(organization_schema: AddOrganization):
    data = lambda model_object, schema_object: model_object(**schema_object.dict())
    return await add_object_to_the_database(data(Organizations, organization_schema))


@organization_router.delete(
    "/by-id/{organization_id}",
    openapi_extra={"descriptions_tag": "organization"},
    description=organization_dcp.ACT_CREATE.value,
    dependencies=[Depends(access_token_verification)],
)
async def delete_organization(organization_id: str):
    return await del_object_to_the_database(Organizations, organization_id)


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
