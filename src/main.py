from fastapi import FastAPI
import uvicorn

from endpoints import main_router


app = FastAPI(docs_url="/doc", redoc_url="/redoc", title="GeoOrg")

app.include_router(main_router)

if __name__ == "__main__":
    app.include_router(main_router)
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
 