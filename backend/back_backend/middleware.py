from prometheus_client import Counter

from fastapi import Request, BackgroundTasks

REQUEST_COUNT = Counter(
    "http_request_count", "TOTAL NUMBER OF REQUESTS",
    ["app_name", "method", "path", "http_status"]
)

async def my_middleware(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(
                        app_name="backend",
                        method=request.method,
                        path=request.url.path,
                        http_status=str(response.status_code)
                        ).inc()
    return response