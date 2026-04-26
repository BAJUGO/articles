from fastapi import FastAPI
from fastapi.responses import Response

from .back_backend.pre_post import lifespan

from .routers.get_post_router import router as get_post_router
from .routers.auth_router import router as auth_router
from .routers.del_patch_router import router as del_patch_router

from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

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


REQUEST_COUNT = Counter("http_requests_total", "HTTP requests total count")

@app.get("/")
async def root():
    REQUEST_COUNT.inc()
    return {"message": "Hello World"}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
