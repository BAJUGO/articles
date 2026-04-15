from fastapi import FastAPI

from .routers.all_test_router import router

app = FastAPI()

app.include_router(router)

