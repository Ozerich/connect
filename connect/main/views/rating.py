#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from pprint import pprint
import datetime


def ajax_rating(request, id, mode):
    rating = Rating.objects.get(id=id)
    if mode == '1':
        rating.plus += 1
    elif mode == '0':
        rating.minus += 1
    rating.save()
    pprint(rating.plus)
    return HttpResponse("")
