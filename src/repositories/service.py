from db.connection import Database


async def check_the_database_for_life() -> dict:
     is_alive = Database()

     return {"code": 200, "message": "service is alive"} if await is_alive.is_alive() else {"code": 500, "message": "service is not alive"} 


 