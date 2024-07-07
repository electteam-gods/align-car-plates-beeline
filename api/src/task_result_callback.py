import schemes
from redisconn import get_redis


def task_result_callback(ch, method, properties, body):
    print(body)
    r = get_redis()
    result = schemes.MQProccessImageResult.model_validate_json(body.decode())
    r.set(result.task_id, result.model_dump_json())
