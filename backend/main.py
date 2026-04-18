from fastapi import FastAPI

from .back_backend.pre_post import lifespan

from .routers.get_post_router import router as get_post_router
from .routers.auth_router import router as auth_router

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(get_post_router)



