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
