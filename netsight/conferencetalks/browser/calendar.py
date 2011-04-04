from plone.memoize import ram
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interfaces import ICalendarSupport
from Products.ATContentTypes.lib import calendarsupport as cs

from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin

from DateTime import DateTime

from netsight.ploneconf2010_talks.talk import calcTime

class ICal(CalendarSupportMixin):

    def __init__(self, context):
        self.context = context

    def getLocation(self):
        return self.context.room

    def CreationDate(self):
        return self.context.CreationDate()

    def start(self):
        return DateTime(calcTime(self.context)[0])

    def end(self):
        return DateTime(calcTime(self.context)[1])

    def contact_name(self):
        return "matt"
        return self.context.name

    def contact_phone(self):
        return None

    def contact_email(self):
        return None

    def event_url(self):
        return self.context.absolute_url()

    def Description(self):
        return self.context.Description().encode('utf-8')

    def Title(self):
        return self.context.Title().encode('utf-8')

    def __getattr__(self, attr):
        return getattr(self.context, attr)

    def UID(self):
        from hashlib import md5
        return md5(self.Title()).hexdigest()

class CalendarView(BrowserView):
    """ view for aggregating event data into an `.ics` feed """

    def update(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        provides = 'netsight.ploneconf2010_talks.talk.ITalk'
        self.events = catalog(path=path, object_provides=provides)

    def render(self):
        self.update()       # collect events                                                                                                 
        context = self.context
        request = self.request
        name = '%s.ics' % context.getId()
        request.RESPONSE.setHeader('Content-Type', 'text/calendar')
        request.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s"' % name)
        request.RESPONSE.write(self.feeddata())

    def feeddata(self):
        context = self.context
        data = cs.ICS_HEADER % dict(prodid=cs.PRODID)
        data += 'X-WR-CALNAME:%s\n' % context.Title()
        data += 'X-WR-CALDESC:%s\n' % context.Description()
        for brain in self.events:
            try:
                data += ICal(brain.getObject()).getICal().decode('utf-8')
            except ValueError:
                pass
        data += cs.ICS_FOOTER
        return data.encode('utf-8')

    __call__ = render

