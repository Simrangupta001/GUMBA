import time

from fastapi import Request

from app.utils.logger import logger


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "%s %s | status=%s | duration=%.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s | status=500 | duration=%.4fs",
            request.method,
            request.url.path,
            duration,
        )

        raise