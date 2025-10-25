from math import cos, pi
from src.repositories.organizations import OrganizationSearchService
from fastapi import HTTPException, status
from src.schemas.organization import SelectOrganization
from src.services.tools import (
    get_object_from_cache_or_function,
    convert_list_of_models_to_dict,
)
from src.repositories.tools import Redis as RedisDB
import json


class CoordinateScope:

    ONE_DEGREES_LATITUDE: float = 111_000

    def __init__(self, latitude: int, longitude: int, radius: int | None = None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    async def calculate_search_area(self) -> tuple[float, float, float, float]:
        if self.radius is None:
            ...

        del_lat = self.radius / CoordinateScope.ONE_DEGREES_LATITUDE
        del_lon = self.radius / (
            CoordinateScope.ONE_DEGREES_LATITUDE * cos(self.latitude * (pi / 180))
        )

        lat_min = self.latitude - del_lat
        lat_max = self.latitude + del_lat
        lon_min = self.longitude - del_lon
        lon_max = self.longitude + del_lon

        return (lat_min, lat_max, lon_min, lon_max)

    @staticmethod
    async def search_organizations_by_geo(
        latitude: float,
        longitude: float,
        radius: int | None = None,
        min_lat: float | None = None,
        max_lat: float | None = None,
        min_lon: float | None = None,
        max_lon: float | None = None,
    ):
        search_range: tuple[float, float, float, float] = (..., ..., ..., ...)
        cache_result = await RedisDB().get_value_by_key(
            key=f"organizations_geo_{latitude}:{longitude}:{radius}:{min_lat}:{max_lat}:{min_lon}:{max_lon}"
        )

        if cache_result is not None:
            print("From cache")
            return json.loads(cache_result)

        if radius is not None and (
            min_lat is not None
            or max_lat is not None
            or min_lon is not None
            or max_lon is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="You can't use radius with other parameters",
                headers={"X-Error": "Use radius or min_lat, max_lat, min_lon, max_lon"},
            )

        if radius is not None:
            search_range = await CoordinateScope(
                latitude, longitude, radius
            ).calculate_search_area()

        else:
            search_range = (min_lat, max_lat, min_lon, max_lon)

        list_organization_by_filter = (
            await OrganizationSearchService.get_list_organizations_in_the_range(
                *search_range
            )
        )
        dict_organizations = convert_list_of_models_to_dict(
            list_organization_by_filter, SelectOrganization
        )

        await RedisDB().set_value_by_key(
            key=f"organizations_geo_{latitude}:{longitude}:{radius}:{min_lat}:{max_lat}:{min_lon}:{max_lon}",
            value=json.dumps(dict_organizations, default=str),
        )

        return list_organization_by_filter
