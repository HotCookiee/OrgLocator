import json
from src.repositories.tools import DataBase, Redis as RedisDB


async def get_object_from_db_or_cache(key: str, object_model, object_schema):
    """Получаем объект из базы данных или кеша"""
    quick_reply = await RedisDB().get_value_by_key(key)
    if quick_reply is not None:
        quick_reply = json.loads(quick_reply)
        print("From cache")
        return quick_reply

    org_inf = await DataBase.get_objects_from_database_by_id_or_name(
        object_model,object_schema, key.split("_")[-1], field=key.split("_")[-2]
    )

    org_inf_dict = object_schema.model_validate(org_inf)

    await RedisDB().set_value_by_key(
        key=f"{object_model.__tablename__.lower()}_{key.split('_')[-2]}_{key.split('_')[-1]}",
        value=org_inf_dict.model_dump_json(),
    )
    print("From DB")
    return org_inf


async def get_object_from_cache_or_function(key: str, fetch_function, *args, **kwargs):
    quick_reply = await RedisDB().get_value_by_key(key)
    if quick_reply is not None:
        quick_reply = json.loads(quick_reply)
        print("From cache")
        return quick_reply

    return await fetch_function(*args, **kwargs)


def convert_list_of_models_to_dict(list_of_models: list, pydantic_schema) -> dict:
    result_dict = {}
    for model in list_of_models:
        model_data = pydantic_schema.model_validate(model)
        result_dict[str(model_data.id)] = model_data.model_dump()
    return result_dict
