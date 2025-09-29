from fastapi import FastAPI
import uvicorn
from uuid import uuid4


from description.health import HealthDescription  as health_dcp
from description.organization import HealthDescription as organization_dcp
from description.selection_by_filter import HealthDescription as selection_by_filter_dcp



from repositories.service import check_the_database_for_life
from repositories.tools import get_objects_from_database
from repositories.buildings import get_list_organization_by_building
from repositories.activities import get_list_organization_by_activity
from repositories.organizations import GetInfoFromOrganization


from models import * 


from schemas.activity import Activity
from schemas.building import Building  
from schemas.organization import Organization  

from services.organizations import CoordinateScope





app = FastAPI(
    docs_url= "/doc",
    redoc_url= "/redoc",
    title="GeoOrg"
)


@app.get("/health/liveness",
         tags          = ["🏥 Эндпоинты для проверки состояния сервиса и базы данных:"],
         openapi_extra = {"descriptions_tag": "health"},
         description   = health_dcp.HEALTH_LIVENESS.value)
async def get_status_liveness_service():
    return {"code": "200", "message": "service is alive"}

@app.get("/health/readiness",
         tags          = ["🏥 Эндпоинты для проверки состояния сервиса и базы данных:"],
         openapi_extra = {"descriptions_tag": "health"},
         description   = health_dcp.HEALTH_DATABASE.value)
async def get_status_liveness_database():
    return  await check_the_database_for_life()
  



@app.get("/organizations/{organization_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"},
         description   = organization_dcp.ORG_GET_BY_ID.value)
async def get_info_organization(organization_id: str):
    org_inf: Organizations = await get_objects_from_database(Organizations,organization_id)
    return org_inf

@app.get("/organizations/building/{building_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"}, 
         description   = organization_dcp.ORG_BY_BUILDING.value)
async def get_list_organization_from_building(building_id: str):
    org_inf: Organizations = await get_list_organization_by_building(building_id)
    return {"code":200,"list_organizations": org_inf}


@app.get("/organizations/activity/{activity_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"},
         description   = organization_dcp.ORG_BY_ACTIVITY.value)
async def get_list_organization_from_activity(activity_id: str):
    org_inf: Organizations = await get_list_organization_by_activity(activity_id)
    return {"code":200,"list_organizations": org_inf}


@app.post("/activity/create/",
          tags          = ["🏢 Работа с организациями:"],
          openapi_extra={"descriptions_tag": "organization"},
          description   = organization_dcp.ORG_CREATE.value)
def create_organization(activity_schema: Activity):
    return {"message": "Hello World"}


@app.post("/buildings/create/",
          tags          = ["🏢 Работа с организациями:"],
          openapi_extra={"descriptions_tag": "organization"},
          description   = organization_dcp.BYL_CREATE.value)
def create_build(build_schema: Building):
    return {"message": "Hello World"}


@app.post("/organizations/create/",
          tags          = ["🏢 Работа с организациями:"],
          openapi_extra={"descriptions_tag": "organization"},
          description   = organization_dcp.ACT_CREATE.value)
def create_activity(organization_schema: Organization):
    return {"message": "Hello World"}


@app.delete("/organizations/delete/{organization_id}",
            tags          = ["🏢 Работа с организациями:"],
            openapi_extra={"descriptions_tag": "organization"},
            description   = organization_dcp.ACT_CREATE.value)
def delete_organization(organization_id: str):
    return {"message": "Hello World"}

@app.delete("/buildings/delete/{building_id}",
            tags          = ["🏢 Работа с организациями:"],
            openapi_extra={"descriptions_tag": "organization"},
            description   = organization_dcp.ACT_CREATE.value)
def delete_build(building_id: str):
    return {"message": "Hello World"}

@app.delete("/activities/delete/{activity_id}",
            tags          = ["🏢 Работа с организациями:"],
            openapi_extra={"descriptions_tag": "organization"},
            description   = organization_dcp.ACT_CREATE.value)
def delete_activity(activity_id: str):
    return {"message": "Hello World"}





@app.get("/organizations/search/geo",
          tags          = ["🔍 Поиск по различным критериям:"],
          openapi_extra = {"descriptions_tag": "selection_by_filter"},
          description   = selection_by_filter_dcp.ORG_SEARCH_GEO.value)
async def get_organization_using_a_filter(latitude: float, longitude: float,  radius: int | None = None,
                                        min_lat: float | None = None, max_lat: float | None = None,
                                        min_lon: float | None = None, max_lon: float | None = None):
        
        return await CoordinateScope.search_organizations_by_geo(latitude, longitude, radius,
                                                                  min_lat, max_lat, min_lon, max_lon)

@app.get("/organizations/search/name/{name}",
         tags          = ["🔍 Поиск по различным критериям:"],
         openapi_extra = {"descriptions_tag": "selection_by_filter"},
         description   = selection_by_filter_dcp.ORG_SEARCH_NAME.value)
async def get_organization_by_name(name_organization: str):

    return await GetInfoFromOrganization.get_info_organization_by_name(name_organization)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
