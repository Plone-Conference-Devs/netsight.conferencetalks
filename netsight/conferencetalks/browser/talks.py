from Products.Five import BrowserView
from plone.intelligenttext.transforms import convertWebIntelligentPlainTextToHtml
from ZTUtils import LazyFilter
from Products.CMFCore.utils import getToolByName

import datetime
from random import shuffle
from hashlib import md5

from netsight.conferencetalks.talk import calcTime


class talks(BrowserView):

    def getTalks(self):
        '''
        All of the code in here is optimized for object access, but I don't want them stored 
        in the folder that this view exists in. So, get all the objects via catalog here and 
        return. Later, update the code to support catalog items.
        '''
        talkObjs = []
        cat = getToolByName(self.context, 'portal_catalog')
        talks = cat(portal_type='netsight.conferencetalks.talk')
        for talk in talks:
            talkObjs.append(talk.getObject())
        return talkObjs    
    
    def talks(self):
        ''' Return all talks in the catalog '''
        talks = self.getTalks()
        keyword = self.request.get('keyword')
        if keyword:
            talks = [ t for t in talks if keyword.strip() in [ x.strip() for x in t.keywords ]]

        shuffle(talks)
        return talks
            

    def votedtalks(self):
        t = self.getTalks()
        t.sort(key=lambda x: talk(x, None).score(), reverse=True)
        return t

class stats(BrowserView):
    def __call__(self):
        res = ""
        for talk in self.getTalks():
            res += talk.country + "\n"

        return res
        # XXX: not sure what this is about
        cats = {}
        authors = []
        for talk in self.getTalks():
            if talk.keywords:
                for keyword in talk.keywords:
                    keyword = keyword.strip()
                    cats[keyword] = cats.get(keyword, 0) + 1

        talks = list(LazyFilter(self.context.contentValues(), skip=''))
        authors = set([ t.name for t in talks ])
        return (len(authors), cats)

class talkUtils:

    def time(self):
        timerange = calcTime(self.context)
        if not timerange:
            return 'Unknown'
        return "%s - %s" % tuple([ x.split()[1] for x in  timerange])

    def description(self):
        return convertWebIntelligentPlainTextToHtml(self.context.description)

    def detail(self):
        return convertWebIntelligentPlainTextToHtml(self.context.detail)

    def bio(self):
        return convertWebIntelligentPlainTextToHtml(self.context.bio)

    def keywords(self):
        return [ x.strip() for x in self.context.keywords ]

    def selected(self):
        req = self.request
        cookie = req.cookies.get('ploneconf2010')
        if not cookie:
            cookie = '%s-%s' % (req.getClientAddr(), datetime.datetime.utcnow().isoformat())
            dt = datetime.datetime.utcnow() + datetime.timedelta(21)
            expires = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
            req.response.setCookie('ploneconf2010', cookie, expires=expires)

        if self.context.votes and cookie in self.context.votes:
            return 1
           
    def getCSSId(self):
        return md5(self.context.getId()).hexdigest()


    def score(self):
        if self.context.votes:
            return len(set(self.context.votes))
        else:
            return 0

class talk(BrowserView, talkUtils):
    pass

class talkView(BrowserView, talkUtils):
    pass

class addvote(BrowserView):
    
    def __call__(self):
        talk = self.context
        votes = talk.votes
        if not votes:
            votes = []

        req = self.request
        cookie = req.cookies.get('ploneconf2010')
        if cookie:
            votes.append(cookie)
            talk.votes = votes
            return "OK"

class schedule(BrowserView):

    pass
