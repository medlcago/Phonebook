import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from config import BASE_DIR
from config import config
from routers import auth_router
from routers import entry_router
from routers import user_router

api_v1_prefix = config.api.api_v1_prefix

app = FastAPI(title="Phone Book API")


@app.get("/", include_in_schema=False)
async def index(request: Request):
    current_path = request.url.path
    redirect_path = current_path + "docs"
    return RedirectResponse(url=redirect_path, status_code=302)


app.mount("/static", StaticFiles(directory=BASE_DIR / "templates/static"), name="static")

app.include_router(auth_router)
app.include_router(user_router, prefix=api_v1_prefix)
app.include_router(entry_router, prefix=api_v1_prefix)

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, port=8080)
