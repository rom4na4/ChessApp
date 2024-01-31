from pydantic import BaseModel, Extra


class RequestData(BaseModel, extra=Extra.allow):
    class Config:
        extra = Extra.allow
