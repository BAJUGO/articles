import time
from prometheus_client import Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

HTTP_REQUEST_DURATION = Histogram(
    "http_requests_total",
    "Duration of HTTP request in seconds",
    labelnames=["method", "path", "status"],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()


        response = await call_next(request)

        route = request.scope.get("route")
        path = route.path_format if route else "not_found"


        duration = time.perf_counter() - start_time

        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            path=path,
            status=response.status_code
        ).observe(duration)

        return response