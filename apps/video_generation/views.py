from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Character
from .utils import *


@login_required
def video_generation(request):
    characters = Character.objects.all()
    context = {"title": "Character Transformation", "characters": characters}
    return render(request, 'video_generation/index.html', context)


@api_view(['POST'])
def transform_character_api(request):
    if django_settings.CHARACTER_TRANSFORMATION_PREMIUM == True:
        return Response({'premium': True}, status=200)
    uploaded_video = request.data.get('video', '')  # json-encoded data
    video_base64 = uploaded_video.split(',')[1]  # Extract the Base64-encoded data portion of the string
    character_id = request.data.get('character', '')

    character = Character.objects.get(id=character_id)
    character_image = image_to_base64(character.image.path)  # base64
    task_id = transform_character(video_base64, character.voice, character_image,
                                  django_settings.CHARACTER_TRANSFORMATION_MODE)
    return Response({'task_id': task_id, }, status=200)


@api_view(['POST'])
def get_status_api(request):
    task_id = request.data.get('task_id', '')
    status = get_status(task_id)
    return Response(status, status=200)


@api_view(['POST'])
def get_video_api(request):
    task_id = request.data.get('task_id', '')
    video_base64 = get_video(task_id)
    video_base64 = 'data:video/mp4;base64,' + video_base64  # Add the data type header to the base64-encoded data
    return Response({'output_video': video_base64, }, status=200)


@login_required
def add_character(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        voice = request.POST.get('voice')
        character = Character(name=name, image=image, voice=voice)
        character.save()
        return redirect('video_generation')
    return render(request, 'video_generation/add_character.html')
