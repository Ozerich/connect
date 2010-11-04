#coding: utf8
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from ..models import *
from ..forms import *
from ..utils import *
import settings
import os


def timetable(req, group, subgroup, week):
	
	if not week:
		week = current_week()
	if not subgroup:
		subgroup = 1
	if not group:
		group = current_user(req).group.name
	content = make_template("timetable.html", 
		groups = Group.objects.all(),
		subgroups = [1,2],
		weeks = [1,2,3,4],
		selected_week = int(week),
		selected_group = group,
		selected_subgroup = int(subgroup),
		timetable_data = parse_timetable(group, subgroup, week),
		)

	return main_template(req, content, title='Рассписание',current=5)
