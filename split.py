#!/usr/bin/python
# -*- coding: utf-8 -*-

from xlrd import *
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


sheet = None



class Lecture:
    def save(self):
        for x in self.subgroups:
            if int(x) > 2:
                self.subgroups.remove(x)
                if not '2' in self.subgroups:
                    self.subgroups.append(2)
                    
        return '<lecture subject="%s" lector="%s" room="%s" start="%s" end="%s" mode="%s" weeks="%s" subgroups="%s"/>' % (
                self.subject, 
                self.lector, 
                self.room, 
                self.start, 
                self.end, 
                self.mode,
                str(self.weeks), 
                str(self.subgroups))



class Day:
    def __init__(self):
        self.lectures = []
        
    def save(self):
        return '<day index="%i">%s</day>' % (self.index, ''.join([x.save() for x in self.lectures]))
        


class Week:
    def __init__(self):
        self.days = []

    def save(self):
        return '<week group="%s" subg="%s" week="%s">%s</week>' % (self.group, self.subgroup, self.week, ''.join([x.save() for x in self.days]))

        
        
def get(x, y):
    return sheet.cell_value(y, x)
    
    
    
def merged_origin(x, y):
    for i in range(0, x+4):
        if len(get(i, y)) > 100:
            return i, y
    return None

    
def parse_lecture(x,y):
    if merged_origin(x,y) is None:
        return parse_lecture_simple(x,y)
    else:
        return parse_lecture_merged(*merged_origin(x, y))
        

def filter_lector(s):
    bl = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    return ' '.join(filter(lambda x: x[0] in bl, s.split()))        
    
    
def parse_lecture_simple(x, y):
    l = Lecture()
    l.subject = get(x+3, y)
    l.mode = get(x+4, y)
    l.room = get(x+5, y)
    l.lector = filter_lector(get(x+6, y))
    l.start, l.end = get(x+1, y).split('-')
    l.weeks = [1, 2, 3, 4]
    if get(x,y) != '':
        l.weeks = [int(w.strip()) for w in get(x,y).split(',')]
    l.subgroups = [1, 2]
    if get(x+2, y) != '':
        l.subgroups = [int(w.strip()) for w in get(x+2, y).split()]
    
    return l


def parse_lecture_merged(x, y):
    data = get(x,y)
    n = ''

    while len(data) > 0:
        if re.match('   .', data):
            data = data[3:]
        else:
            n += data[0]
            data = data[1:]
    data = n.strip().replace('  ', ' ')

    l = Lecture()
    l.weeks = [1, 2, 3, 4]
    if get(x-3,y) != '':
        l.weeks = [int(w.strip()) for w in get(x-3,y).split(',')]
    l.start, l.end = get(x-2, y).split('-')
    
    l.subgroups = [1, 2]

    data = data.split()
    if len(data) == 4:
        l.subject = ' '.join(data[0:2])
        l.mode = ''
        l.room = ''
        l.lector = ''
        if 'ауд.' in data:
            l.room = data[data.index('ауд.')+1]
    else:
        l.subject = data[0]
        l.mode = data[1]
        l.room = data[3]
        l.lector = filter_lector(' '.join(data[4:]))
    
    return l


def parse_day(x, y, h, idx):
    d = Day()
    d.index = idx
    for r in range(y, h):
        if get(x + 3, r) != '' or (merged_origin(x+3, r) is not None):
            try:
                d.lectures.append(parse_lecture(x, r))
            except:
                pass
    return d
  
  
  
def parse_week(x, y):
    r = y
    last_hour = 23
    start = y
    day = 0
    week = Week()
    while r < sheet.nrows:
        if get(x+1, r) != '' or (merged_origin(x+1,r) is not None):
            if merged_origin(x+1,r) is not None:
                xx, yy = merged_origin(x+1,r)
                hr = int(get(xx - 2, yy).split(':')[0])
            else:
                hr = int(get(x+1,r).split(':')[0])
            if hr < last_hour:
                if start != r:
                    week.days.append(parse_day(x, start, r, day))
                    day += 1
                    start = r
            last_hour = hr
        r += 1
    week.days.append(parse_day(x, start, r, day))
    return week
    
    
                            
# Load sheet        
book = open_workbook(sys.argv[1], formatting_info=True, encoding_override='cp1251')
sheet = book.sheet_by_index(0)
    
   
# Find groups
idx = 0
for i in range(1, sheet.ncols):
    cv = get(i, 3)
    if cv != '':
        id = cv.split()[-1]
        print 'Parsing group %s' % id
        
        week = parse_week(1+idx*7, 5)
        
        # Split in four
        for wd in range(1,5):
            # Split in two
            for x in range(1,3):
                nw = Week()
                nw.week = str(wd)
                nw.group = id
                nw.subgroup = str(x)
                for d in week.days:
                    nd = Day()
                    nd.index = d.index
                    nw.days.append(nd)
                    for l in d.lectures:
                        if (wd in l.weeks) and (x in l.subgroups):
                            nd.lectures.append(l)
                open('timetable/%s-%i-%i.xml'%(id,x,wd), 'w').write(nw.save())
                    
            
        idx += 1
      
      
