from fastapi import FastAPI
import uvicorn

from description.health import HealthDescription  as health_dcp
from description.organization import HealthDescription as organization_dcp
from description.selection_by_filter import HealthDescription as selection_by_filter_dcp


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
    return {"message": "Hello World"}

@app.get("/health/readiness",
         tags          = ["🏥 Эндпоинты для проверки состояния сервиса и базы данных:"],
         openapi_extra =  {"descriptions_tag": "health"},
         description   = health_dcp.HEALTH_DATABASE.value)
async def get_status_liveness_database():
    return {"message": "Hello World"}
  



@app.get("/organizations/{organization_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"},
         description   = organization_dcp.ORG_GET_BY_ID.value)
async def get_info_organization(organization_id: int):
    return {"message": "organization_id"}

@app.get("/organizations/building/{building_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"},
         description   = organization_dcp.ORG_BY_BUILDING.value)
async def get_list_organization_from_building(building_id: int):
    return {"message": f"{building_id}"}


@app.get("/organizations/activity/{activity_id}",
         tags          = ["🏢 Работа с организациями:"],
         openapi_extra = {"descriptions_tag": "organization"},
         description   = organization_dcp.ORG_BY_ACTIVITY.value)
async def get_list_organization_from_activity(activity_id: int):
    return {"message": f"{activity_id}"}




@app.post("/organizations/search/geo",
          tags          = ["🔍 Поиск по различным критериям:"],
          openapi_extra = {"descriptions_tag": "selection_by_filter"},
          description   = selection_by_filter_dcp.ORG_SEARCH_GEO.value)
async def get_organization_using_a_filter():
    return {"message": "Hello World"}

@app.get("/organizations/search/name/{name}",
         tags          = ["🔍 Поиск по различным критериям:"],
         openapi_extra = {"descriptions_tag": "selection_by_filter"},
         description   = selection_by_filter_dcp.ORG_SEARCH_NAME.value)
async def get_organization_by_name(name: str):
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
