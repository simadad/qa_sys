from django.shortcuts import render
from .models import *
# Create your views here.


def item_save(request):
    title = request.POST.get('title')
    answer = request.POST.get('answer')
    item, is_new = QAItem.objects.get_or_create(
        title=title,
        answer=answer
    )
    return is_new
