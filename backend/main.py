from fastapi import FastAPI

from .back_backend.pre_post import lifespan

from .routers.get_post_router import router as get_post_router
from .routers.auth_router import router as auth_router
from .routers.del_patch_router import router as del_patch_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(get_post_router)
app.include_router(del_patch_router)




origins = [
    "http://localhost",
    "http://localhost:80",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )