import uvicorn
from fastapi import FastAPI

from config import config
from routers import auth_router
from routers import entry_router
from routers import user_router

api_v1_prefix = config.api.api_v1_prefix

app = FastAPI(title="Phone Book API")

app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(user_router, prefix=api_v1_prefix)
app.include_router(entry_router, prefix=api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run(app, port=8080)
