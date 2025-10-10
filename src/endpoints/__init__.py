from fastapi import APIRouter
from .activities import activity_router
from .buildings import building_router
from .health import health_router
from .organizations import organization_router
from .users import user_router


main_router = APIRouter()

main_router.include_router(
    health_router,
    prefix="/health",
    tags=["🏥 Эндпоинты для проверки состояния сервиса и базы данных:"],
)
main_router.include_router(
    organization_router, prefix="/organizations", tags=["🏢 Работа с организациями:"]
)
main_router.include_router(
    building_router, prefix="/buildings", tags=["🏢 Работа с зданиями:"]
)
main_router.include_router(
    activity_router, prefix="/activities", tags=["🏢 Работа с активностями:"]
)
main_router.include_router(user_router, prefix="/users", tags=["Пользователи"])
