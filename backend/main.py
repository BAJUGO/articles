from fastapi import FastAPI

from .back_backend.pre_post import lifespan

from .routers.all_test_router import router

app = FastAPI(lifespan=lifespan)

app.include_router(router)



