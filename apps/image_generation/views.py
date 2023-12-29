from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import *


@login_required
def image_generation(request):
    context = {"title": "Image Generation"}
    return render(request, 'image_generation/index.html', context)


@api_view(['POST'])
def generate_image_api(request):
    if django_settings.IMAGE_GENERATION_PREMIUM == True:
        return Response({'premium': True}, status=200)
    text_prompt = request.data.get('text_prompt', '')  # json-encoded data
    task_id = generate_image(text_prompt, django_settings.IMAGE_GENERATION_STEPS)
    print(f"{text_prompt = }")  # log to console
    return Response({'text_prompt': text_prompt, 'task_id': task_id}, status=200)


@api_view(['POST'])
def get_status_api(request):
    task_id = request.data.get('task_id', '')
    result = get_status(task_id)
    return Response(result, status=200)


@api_view(['POST'])
def get_image_api(request):
    task_id = request.data.get('task_id', '')
    result = get_image(task_id)
    return Response(result, status=200)
