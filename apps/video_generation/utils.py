import base64
import json

import requests
from django.conf import settings as django_settings

url = django_settings.VIDEO_GENERATION_API_URL


# function to get base64 from image name
def image_to_base64(image):
    with open(image, "rb") as image_file:
        image = image_file.read()
        image_base64 = base64.b64encode(image).decode('utf-8')
    return image_base64


def transform_character(video, character_name, character, mode):
    data = {"video": video, "character_name": character_name, "character": character, "mode": mode}
    response = requests.post(url + "transform_character", json=data)
    try:
        task_id = json.loads(response.content.decode('utf-8'))['task_id']
    except Exception as error:
        raise Exception("Video Generation Server Error, Check the Server Link")
    return task_id


def get_status(task_id):
    data = {"task_id": task_id}
    response = requests.post(url + "status", json=data)
    response = json.loads(response.content.decode('utf-8'))
    try:
        status = response['status']
        if status == "PENDING":
            remaining_tasks = response['remaining_tasks']
            return {"status": status, "remaining_tasks": remaining_tasks}
    except Exception as error:
        raise Exception("Video Generation Server Error, Check the Server Link")
    return {"status": status}


def get_video(task_id):
    data = {"task_id": task_id}
    response = requests.post(url + "get_video", json=data)
    response = json.loads(response.content.decode('utf-8'))
    try:
        video_base64 = response['output_video']
    except Exception as error:
        raise Exception("Video Generation Server Error, Check the Server Link")
    return video_base64
