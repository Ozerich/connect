from django.template import Context, loader
from django.http import HttpResponse
from models import *
import settings
import os
import Image
import datetime
from pprint import pprint
from lxml import etree


def init(request):
    try: 
        request.user = User.objects.get(email=request.session['user'])
    except:
        request.user = None
    request.templatevars = {
        'me': request.user,
        'has_menu': True,
        'friend_request_count': friend_request_count(request),
        'unread_messages_count': unread_messages_count(request),
        'days': range(1,32),
        'months': range(1,13),
        'years': xrange(2010,1970,-1),
        'langs': Language.objects.all(),
    }

def make_template(request, template, **kwargs):
    t = loader.get_template(template)
    kwargs.update(request.templatevars)
    c = Context(kwargs)
    return t.render(c)

def login_user(request, user):
    request.session['user'] = user

def logged_in(request):
    return 'user' in request.session
    
def make_paginator(req, l, pl, st, link):
    return make_template(
            req,
            'paginator.html',
            pages=range(1,(l+pl-1)/pl+1),
            link=link,
            current=st/pl+1
        )
           
def download_file(file, *path):
    srcf = os.path.join(settings.STORAGE_PATH, *path)
    open(srcf, 'w').write(file.read())
    return srcf

def resize_image(file, size, path):
    img = Image.open(file)
    img.thumbnail((size, size), Image.ANTIALIAS)
    img.save(path)

def unread_messages_count(request):
    cu = request.user
    c = len(Message.objects.filter(owner=cu, unread=1))
    return c if c > 0 else ''

def friend_request_count(request):
    c = 0
    cu = request.user
    for fs in Friendship.objects.filter(dst=cu):
        try:
            Friendship.objects.get(src=cu, dst=fs.src)
        except Friendship.DoesNotExist:
            c += 1
    return c if c > 0 else ''
    
def delete_avatar(user):
    if user.avatar != 'default.png':
        try:
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '100.' + user.avatar))
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '50.' + user.avatar))
            os.unlink(os.path.join(settings.STORAGE_PATH, 'avatars', '25.' + user.avatar))
        except:
            pass
    user.avatar = 'default.png'
    user.save()
        
def save_avatar(request, user):
    delete_avatar(user)
    f = request.FILES['avatar']
    ext = f.name.split('.')[-1]
    fn = str(user.id) + '.' + ext
    srcf = download_file(f, 'avatars',  fn)
    resize_image(
        srcf,
        100,
        os.path.join(settings.STORAGE_PATH, 'avatars', '100.'+fn)
    )
    resize_image(
        srcf,
        50,
        os.path.join(settings.STORAGE_PATH, 'avatars', '50.'+fn)
    )
    resize_image(
        srcf,
        25,
        os.path.join(settings.STORAGE_PATH, 'avatars', '25.'+fn)
    )
    os.unlink(srcf)
    user.avatar = fn

def current_week():
    today_date = datetime.date.today()
    begin_study_date = datetime.date(2010, 8, 30)
    days_dif = today_date - begin_study_date
    weeks_dif = (divmod(days_dif.days, 7)[0] + 1) % 4;
    return weeks_dif

def timetable_filename(group, subgroup, week):
    filename = "../timetable/" + group + "-" + str(subgroup) + "-" + str(week) + ".xml"
    return filename

class Lecture:
    def __repr__(self):
        return str(self.__dict__)

def parse_timetable(group, subgroup, week):
    filename = timetable_filename(group, subgroup, week)
    xml = etree.parse(filename)
    root = xml.getroot()
    result = []
    for day_index in range(0, len(root)):
        day = root[day_index]
        result_day = []
        for lecture_index in range(0, len(day)):
            lecture = day[lecture_index]
            result_lecture = Lecture()
            result_lecture.subject_name = lecture.get("subject")
            result_lecture.lector = lecture.get("lector")
            try:
                l = Lector.objects.get(full_name=lecture.get("lector"))
                result_lecture.lector_id = l.id
            except Lector.DoesNotExist:
                pass
            result_lecture.start = lecture.get("start")
            result_lecture.end = lecture.get("end")
            result_lecture.room = lecture.get("room")
            result_lecture.mode = lecture.get("mode")
            result_day.append(result_lecture);
        result.append(result_day)
    return result

def tomorrow_week():
	today_date = datetime.date.today()
	tomorrow_date = today_date + datetime.timedelta(days=1)
	tomorrow_weekday = tomorrow_date.weekday()
	tomorrow_week = current_week()
	if tomorrow_weekday == 0:
		tomorrow_week += 1
	return tomorrow_week
	
def tomorrow_timetable(request):
	today_date = datetime.date.today()
	tomorrow_date = today_date + datetime.timedelta(days=1)
	tomorrow_weekday = tomorrow_date.weekday()
	user = request.user
	timetable_data = parse_timetable(user.group.name, user.subgroup, tomorrow_week())
	if (tomorrow_weekday) < len(timetable_data):
		return timetable_data[tomorrow_weekday]
	else:
		return []
 
def my_events(request):
    communities = request.user.communities.all()
    events = []
    for community in communities:
        c_e = Event.objects.filter(community=community).order_by("event_date")
        for event in c_e:
            events.append(event)
    
    result = []
    current_date = 0
    result_item = []
    
    for event in events:
        if event.event_date == current_date:
            result_item.append(event)
        else:
            if len(result_item) != 0:
                result.append({"date" : result_item[0].event_date, "items" : result_item})
            result_item = []
            result_item.append(event)
            current_date = event.event_date
    if len(result_item) != 0:
        result.append({"date" : result_item[0].event_date, "items" : result_item})     
    return result
