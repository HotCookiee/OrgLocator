from fastapi import FastAPI

from src.endpoints import main_router


app = FastAPI(docs_url="/doc", redoc_url="/redoc", title="GeoOrg")

app.include_router(main_router)

if __name__ == "__main__":
    app.include_router(main_router)
