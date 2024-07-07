from pydantic import BaseModel
from typing import Optional


class MQProcessImageTask(BaseModel):
    task_id: str
    image_url: str


class MQProccessImageResult(BaseModel):
    task_id: str
    status: str
    result_url: Optional[str] = None
