#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

def lector(request, id):
    l = Lector.objects.get(id=id)
   
    
    content = make_template("lector.html",
            lector=l,
        )
    return main_template(request, content, 0, u"Преподаватель " + l.full_name)
