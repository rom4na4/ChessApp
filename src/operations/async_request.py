import json

import httpx
from celery import Celery
from fastapi import Request
from src.backups.config import const, db_broker
from src.models.all_models import RequestData
from src.operations.async_log import logging_job

celery_manager = Celery('Task queue', broker=db_broker)


@celery_manager.task
async def send_http_request(data: RequestData, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            request_data_all = {"token": request.headers.get("authorization"), "rb": data.model_dump()}
            encoded_data = json.dumps(request_data_all, ensure_ascii=False)
            response = await client.post(const[0], data=encoded_data)
            if response.status_code in [200, 201, 202, 204]:
                await logging_job(request.client.host, str(request.client.port), response.status_code, request.method,
                                  response.text)
                return response
            elif response.status_code in [500, 501, 503, 520]:
                if response.status_code == 500:
                    raise TimeoutError("Timeout. Server isn't reachable or Internal Server error.")
                else:
                    raise TimeoutError(response.status_code, "Internal Server error. Message:",
                                       response.content.decode('utf-8'))
            elif response.status_code in [400, 401, 403, 405, 409, 415, 422, 429]:
                raise ValueError("Value Error. Bad request")
        except TimeoutError as e:
            await logging_job(request.client.host, str(request.client.port), 500, request.method, e.args[0])
            return response
        except ValueError as e:
            await logging_job(request.client.host, str(request.client.port), 400, request.method, e.args[0])
            return response
        except Exception as e:
            await logging_job(request.client.host, str(request.client.port), str(500), request.method, e.args[0])
            return response
