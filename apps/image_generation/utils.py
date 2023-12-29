import json

import requests
from django.conf import settings as django_settings

url = django_settings.IMAGE_GENERATION_API_URL


def generate_image(text_prompt: str, steps: int):
    data = {"prompt": text_prompt, "num_inference_steps": steps, }

    response = requests.post(url + "generate_image", json=data)
    try:
        task_id = json.loads(response.content.decode('utf-8'))['id']
    except Exception as error:
        raise Exception("Image Generation Server Error, Check the Server Link")
    return task_id


def get_status(task_id: int):
    data = {"task_id": task_id}
    response = requests.post(url + "get_status", json=data)
    response = json.loads(response.content.decode('utf-8'))
    try:
        status = response['status']
        if status == "Pending":
            remaining_tasks = response['remaining_tasks']
            return {"status": status, "remaining_tasks": remaining_tasks}
    except Exception as error:
        raise Exception("Image Generation Server Error, Check the Server Link")
    return {"status": status}


def get_image(task_id: int):
    data = {"task_id": task_id}
    response = requests.post(url + "get_image", json=data)
    response = json.loads(response.content.decode('utf-8'))
    try:
        image_base64 = response['image_base64']
    except Exception as error:
        raise Exception("Image Generation Server Error, Check the Server Link")
    return {"image_base64": image_base64}
