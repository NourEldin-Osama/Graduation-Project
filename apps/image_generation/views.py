import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import generate_image

# Create your views here.


def image_generation(request):
    context = {"title": "Image Generation"}
    return render(request, 'image_generation/index.html', context)


@api_view(['POST'])
def image_generation_api(request):
    # text_prompt = request.POST.get('text_prompt', '')  # form-encoded data
    text_prompt = request.data.get('text_prompt', '')  # json-encoded data
    image_base64 = generate_image(text_prompt, 25)
    print(f"{text_prompt = }")  # log to console
    return Response({'image_base64': image_base64}, status=200)
