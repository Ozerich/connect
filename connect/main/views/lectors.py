#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

def lectors(request):
    lectors_data = Lector.objects.all()
    content = make_template('lectors.html',
        lectors=lectors_data,)
    return main_template(
        request, 
        content, 
        title='Преподаватели',
        current=3
    )
