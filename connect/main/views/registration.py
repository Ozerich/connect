#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

import datetime



def registration(request):
    error = None
    if request.POST:
        try:
            User.objects.get(number=request.POST['private_number'])
            error = 'Пользователь с таким студенческим билетом уже существует'
        except User.DoesNotExist:
            pass
        try:
            User.objects.get(email=request.POST['email'])
            error = 'Пользователь с таким e-mail уже существует'
        except User.DoesNotExist:
            pass

        if not error:
            u = User(
                    email = request.POST['email'],
                    password = request.POST['password'],
                    name = request.POST['name'],
                    surname = request.POST['surname'],
                    number = request.POST['private_number'],
                    group = Group.objects.get(name=request.POST['group']),
                    subgroup = int(request.POST['subgroup']),
                    language = Language.objects.get(name=request.POST['language']),
                    birthday = datetime.date(
                        int(request.POST['birth_year']),
                        int(request.POST['birth_month']),
                        int(request.POST['birth_day']),
                    ),
                    avatar = 'default.png'
                )
            if 'avatar' in request.FILES:
                save_avatar(request, u)
            u.save()
            login_user(request, u.email)
            return HttpResponseRedirect('/')
        
    content = make_template(
        'registration-form.html',
            error_msg = error,
            days = range(1,32),
            months = range(1,13),
            years = xrange(2010,1970,-1),
            groups = Group.objects.all(),
            langs =  Language.objects.all()
    )
    
    return render_to_response(
        'main.html',
        {
            'content': content,
            'page_title': 'Регистрация',
        }
    )
