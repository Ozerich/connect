#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

def lectors(request):
    init(request)
    return HttpResponse(make_template(
        request, 
        'lectors.html', 
        lectors=Lector.objects.all(),
        title='Преподаватели',
        current=3
    ))
