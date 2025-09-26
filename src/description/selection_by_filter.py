from enum import Enum


class HealthDescription(Enum):
    ORG_SEARCH_GEO  = "Поиск организаций по географическим координатам. Принимает координаты и радиус поиска."
    ORG_SEARCH_NAME = "Поиск организаций по названию. Поддерживает частичное совпадение."
    
