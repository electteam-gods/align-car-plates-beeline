from fastapi import FastAPI, APIRouter, UploadFile
from fastapi.responses import JSONResponse
import pika
import redis
from uuid import uuid4
from task import TaskStatuses
from requests import request

import schemes
from redisconn import get_redis
import boto3

# publisherConnection = pika.BlockingConnection(
#     pika.ConnectionParameters(
#         host="rabbitmq", credentials=pika.PlainCredentials("rmuser", "rmpassword")
#     )
# )
# publisherChannel = publisherConnection.channel()
# publisherChannel.queue_declare(queue="task_queue", durable=True)

app = FastAPI()
router = APIRouter(prefix="/api")


@router.post("/process")
async def process(files: list[UploadFile]):

    s3_client = boto3.client(
        "s3",
        region_name="ru-1",
        aws_access_key_id="BLZVPJ5JNCHVJZPR6SU3",
        aws_secret_access_key="1dwymiu3T0y95gQSm3ivnQHnqHqatJPAyZIyqA4p",
        endpoint_url="https://s3.timeweb.cloud"
    )

    results = schemes.ProcessResults(list=[])
    
    data = request('post', 'http://ai-model/', data={})

    id = str(uuid4())
    # upload to s3
    for file in files:
        s3_key = id + file.filename
        s3_client.put_object(
            Bucket="516d5635-4ecebcb3-728f-458d-a2e8-786f8949b0d2",
            Key=s3_key,
            Body=file.file,
        )
        task = schemes.MQProcessImageTask(
            task_id=id,
            image_url=f"https://s3.timeweb.cloud/516d5635-4ecebcb3-728f-458d-a2e8-786f8949b0d2/{s3_key}",
        )

        # publisherChannel.basic_publish(
        #     exchange="",
        #     routing_key="task_queue",
        #     body=task.model_dump_json(),
        #     properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        # )
        taskResult = schemes.MQProccessImageResult(
            task_id=task.task_id, status=TaskStatuses.Accepted.name
        )
        r = get_redis()
        r.set(task.task_id, taskResult.model_dump_json())
        results.list.append(taskResult)
    return results




@router.get("/result")
async def check_status(task_id: str):
    r = get_redis()
    result = r.get(task_id)
    if result is None:
        return JSONResponse({"task_id": task_id, "status": TaskStatuses.Canceled.name})

    result = schemes.MQProccessImageResult.model_validate_json(result)
    return result


app.include_router(router)
