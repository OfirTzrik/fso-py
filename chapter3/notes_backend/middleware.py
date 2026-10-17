import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# A "middleware" is a function that works with every request
# before it is processed by any specific path operation. And also
# with every response before returning it.
# Middleware should be used for things that apply to all requests,
# such as logging, timing, etc. ("middleware" will be registered
# by main.py)
async def log_requests(request: Request, call_next):
	"""Log the request and response time"""
	start = time.perf_counter()
	# Code before runs before the matching route
	response = await call_next(request)
	# Code after runs after the matching route
	ms = (time.perf_counter() - start) * 1000
	logger.info(f"{request.method} {request.url.path} {response.status_code} {ms:.1f} ms")
	return response


# OperationalError is raised whenever SQLAlchemy can't reach the
# database or the connection break (Registered by main.py)
def database_unavailable(request: Request, exc):
	'''Database unreachable or connection broke, return "503
	Service Unavailable" with a readable message instead of
	the generic "500 Internal Server Error"'''
	logger.error(f"database error: {exc.orig}")
	# JSON Response builds a response by hand
	return JSONResponse(status_code=503, content={"detail": "database unavailable"})
