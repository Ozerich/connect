#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *

import datetime


def index(request):
    init(request)
    if logged_in(request):
        if request.POST:
            u = req.user
            u.email = request.POST['email']
            u.birthday = datetime.date(
                int(request.POST['birth_year']),
                int(request.POST['birth_month']),
                int(request.POST['birth_day']),
            )
            u.language = Language.objects.get(name=request.POST['language'])

            if request.POST['password_new'] != '':
                u.password = request.POST['password_new']

            if 'avatar' in request.FILES:
                save_avatar(request, u)
            if 'deleteavatar' in request.POST:
                delete_avatar(u)
            u.save()

        tomorrow_data = tomorrow_timetable(request)

        events = my_events(request)
        
        return HttpResponse(make_template(
            request,
            'dashboard.html',
            current=1,
            events=events,
			week_number = tomorrow_week(),
            tomorrow_timetable = tomorrow_data,
            title='Домашняя'
        ))
    else:
        return HttpResponseRedirect('/login')
        
