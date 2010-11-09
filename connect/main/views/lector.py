#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
from datetime import *

def lector(request, id):
    init(request)
    l = Lector.objects.get(id=id)
    return HttpResponse(make_template(
        request,
        "lector.html",
        lector=l,
        current=3,
        title=l.full_name
    ))

def lector_comment(request, id):
	text = request.POST['text']
	comment = LectorComment()
	comment.text = text
	comment.author = current_user(request)
	comment.date = datetime.now()
	comment.lector = Lector.objects.get(id=id)
	comment.save()
	
	return HttpResponseRedirect('/lector/%s' % id)
