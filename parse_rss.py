import sys

if sys.version_info.major == 2:

    from urllib2 import urlopen
    from UserList import UserList
    from UserDict import UserDict

else:
    
    from urllib.request import urlopen
    from collections import UserList, UserDict


import datetime
import json
import xml.etree.ElementTree as ET


def get_data_json(url):
    return json.load(urlopen(url))


def get_datetime(string):
    FORMAT = "%a, %d %b %Y %H:%M:%S"
    #string = 'Tue, 27 Sep 2016 14:24:26 +0100' 
    #len('Tue, 27 Sep 2016 14:24:26') == 25
    string = string[:25] #%z not supproted in python 2
    return datetime.datetime.strptime(string, FORMAT)


#TODO beautifulsoup over xml...??? description is in html...

class RssDocument(UserDict):

    def __init__(self, d):
        d['date'] = get_datetime(d['pubDate']) 
        d['title'] = d['title'].encode('utf8')
        d['description'] = d['description'].encode('utf8')
        UserDict.__init__(self, dict=d)

    @property
    def date(self):
        return self["date"]

    @property
    def description(self):
        return self["description"]

    @property
    def author(self):
        return self["author"]

    @property
    def title(self):
        return self["title"]

    def __lt__(self, other):
        return self.date < other.date

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return "{} at {}".format(self.title, self.date)

    def str_full(self):
        return  "{}\n{} by {}\n".format(self, self.description, self.author)
         
    def str_conditional(self, date):
        return '' if self.date < date else self.str_full()
 
         

class RssDocuments(UserList):
    def __init__(self, initlist):
        initlist = sorted(RssDocument(d) for d in initlist)
        UserList.__init__(self, initlist=initlist)

    def documents_onwards(self, date):
        return [d for d in self if d.date > date]


def get_data_rss(url): 
    
#KEYS = [u'title', u'description', u'link', u'author', u'guid', u'category', u'pubdate']

    keys = ['pubDate', 'author', 'title', 'description']

    root = ET.fromstring(urlopen(url).read())

    items = [{k:e.find(k).text for k in keys} for e in root.find('channel').findall('item')]

    return RssDocuments(items)

