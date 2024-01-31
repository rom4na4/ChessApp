import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError, HTTPException, ValidationException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.backups.config import origins
from src.models.all_models import RequestData
from src.operations.async_log import logging_job
from src.operations.async_request import send_http_request

app = FastAPI(title="ChessAPI 0.1")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
async def read_root():
    return "Hi  #ChessAPI 1.0 "


@app.post("/api/")
async def send_data(data: RequestData, request: Request):
    response = await send_http_request(data, request)
    return Response(
        status_code=response.status_code,
        headers=response.headers,
        media_type="application/json",
        content=response.content
    )


@app.get("/api/logs")
async def logs_list(request: Request, logs: str):
    if request.headers.get("logs") == 'fdsflkef!232ljkflkjf435@33rrgreg' or logs == 'fdsflkef!232ljkflkjf435@33rrgreg':
        with open('src/backups/debug.log') as file:
            text = file.read()
            return JSONResponse(status_code=200, content=text)
    else:
        return Response(status_code=400, content="Bad request")


# Обработка общих ошибок:
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    await logging_job(request.client.host, str(request.client.port), 422, request.method,
                      '"fast_message": "validation error"')
    return JSONResponse(
        status_code=422,
        content={"fast_message": "validation error"},
    )


# Обработка ошибок, связанных с аутентификацией:
@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    await logging_job(request.client.host, str(request.client.port), exc.status_code, request.method,
                      '"fast_message": "authentication error"')
    return JSONResponse(
        status_code=exc.status_code,
        content={"fast_message": "authentication error"},
    )


# Обработка ошибок, связанных с HTTP:
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    await logging_job(request.client.host, str(request.client.port), exc.status_code, request.method,
                      '"fast_message": "HTTP error"')
    return JSONResponse(
        status_code=exc.status_code,
        content={"fast_message": "HTTP error"},
    )


# Обработка ошибок, связанных с валидацией:
@app.exception_handler(ValidationException)
async def validation_error_exception_handler(request: Request, exc: ValidationException):
    await logging_job(request.client.host, str(request.client.port), 422, request.method,
                      '"fast_message": "validation error"')
    return JSONResponse(
        status_code=422,
        content={"fast_message": "validation error"},
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=44000, log_level="info")
