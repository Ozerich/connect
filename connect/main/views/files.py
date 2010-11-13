#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
import settings
import os
from datetime import *


def file_download(req, id):
    init(req)
    file = File.objects.get(id=id)
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    response.write(open(os.path.join(settings.STORAGE_PATH, 'files', id)).read())
    return response

def file_delete(req, id):
    init(req)
    file = File.objects.get(id=id)
    if file.author == req.user:
        file.delete()
        file_name = os.path.join(settings.STORAGE_PATH, 'files', id)
        if os.path.exists(file_name):
            os.unlink(file_name)
    return HttpResponseRedirect('/files')
    
def file_add(request):
    init(request)
    upload_file = request.FILES['file']
    
    file = File(
        name = upload_file.name,
        date = datetime.now(),
        author = request.user,
        description = request.POST['description'],
    )
    file.save()
    
    download_file(upload_file, "files", str(file.id))
    
    return HttpResponseRedirect('/files')
    
def files(req):
    init(req)
    cu = req.user

    ff = File.objects.filter(author=cu)


    return HttpResponse(make_template(
        req, 
        'files.html',
        files=ff,
        title='Файлы',
        current=1
    ))

