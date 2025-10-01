from math import cos, pi
from repositories.organizations import OrganizationSearchService


class CoordinateScope():
    
    ONE_DEGREES_LATITUDE: float = 111000
    
    def __init__(self,latitude: int, longitude: int,  radius: int | None  = None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius



    async def calculate_search_area(self)-> tuple[float,float,float,float]:
            if (self.radius is None):
                ...

            del_lat = self.radius / CoordinateScope.ONE_DEGREES_LATITUDE
            print(del_lat)
            del_lon = (self.radius / (CoordinateScope.ONE_DEGREES_LATITUDE * cos(self.latitude * (pi / 180))))
            
            lat_min = self.latitude - del_lat
            lat_max = self.latitude + del_lat
            lon_min = self.longitude - del_lon
            lon_max = self.longitude + del_lon


            return (lat_min,lat_max,lon_min,lon_max)
    
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
        search_range:tuple[float,float,float,float] = (..., ..., ..., ...)

        if radius is not None and (min_lat is not None or max_lat is not None or min_lon is not None or max_lon is not None):
            return {"code:":"500","Message":"error"}

        elif radius is not None:
            search_range = await CoordinateScope(latitude, longitude,  radius).calculate_search_area()

        else: 
            search_range = (min_lat,max_lat,min_lon,max_lon)


        list_organization_by_filter = await OrganizationSearchService.get_list_organizations_in_the_range(*search_range)


        return list_organization_by_filter

