#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
import settings
import os


def file_download(req, id):
    file = File.objects.get(id=id)
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    response.write(open(os.path.join(settings.STORAGE_PATH, 'files', id)).read())
    return response

def file_delete(req, id):
    file = File.objects.get(id=id)
    if file.author == current_user(req):
        file.delete()
        os.unlink(os.path.join(settings.STORAGE_PATH, 'files', id))
    return HttpResponseRedirect('/files')
    
    
def files(req):
    cu = current_user(req)

    ff = File.objects.filter(author=cu)
        
    content = make_template(
        'files.html',
        files=ff,
    )
    return main_template(
        req, 
        content, 
        title='Файлы',
        current=1
    )
