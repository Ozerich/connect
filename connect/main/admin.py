#coding: utf8
from main.models import *
from django.contrib import admin
        
        
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Личные', {'fields': ['name', 'surname', 'birthday']}),
        ('Регистрационные данные', {'fields': ['email', 'password']}),
        ('Учеба', {'fields': ['number', 'group', 'subgroup', 'language']}),
        ('Группы', {'fields': ['communities']}),
        ('Внутреннее', {'fields': ['avatar']}),
    ]
    search_fields = ['email', 'name', 'surname']


admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(Language)
admin.site.register(Faculty)
admin.site.register(Stream)
admin.site.register(Friendship)
admin.site.register(Community)

