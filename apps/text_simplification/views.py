from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import *


@login_required
def text_simplification(request):
    context = {"title": "Text Simplification"}
    return render(request, 'text_simplification/index.html', context)


@api_view(['POST'])
def text_simplification_api(request):
    if django_settings.TEXT_SIMPLIFICATION_PREMIUM == True:
        return Response({'premium': True}, status=200)
    # original_text = request.POST.get('input_text', '')  # form-encoded data
    original_text = request.data.get('input_text', '')  # json-encoded data
    simplified_text = simplify_text(original_text, model='chatgpt')
    print(f"{original_text = }")
    print(f"{simplified_text = }")
    return Response({'original_text': original_text, 'simplified_text': simplified_text}, status=200)
