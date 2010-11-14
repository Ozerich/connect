#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

import datetime


def login(request):
    error = None
    if request.POST:
        try:
            u = User.objects.get(
                email=request.POST['email'],
                password=request.POST['password'],
            )
            login_user(request, u.email)
            return HttpResponseRedirect('/')
        except User.DoesNotExist:
            error = 'Неверный e-mail или пароль'
    
    return render_to_response(
        'main-login.html',
        {
            'error_msg': error,
            'page_title': 'Connect',
        }
    )
    
def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return HttpResponseRedirect('/')

