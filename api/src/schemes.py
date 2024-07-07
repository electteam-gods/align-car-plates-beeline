from pydantic import BaseModel, HttpUrl
from typing import Optional


class ProccessInput(BaseModel):
    image_url: HttpUrl


class MQProcessImageTask(BaseModel):
    task_id: str
    image_url: str


class MQProccessImageResult(BaseModel):
    task_id: str
    status: str
    result_url: Optional[str] = None


class ProcessResults(BaseModel):
    list: list[MQProccessImageResult]
