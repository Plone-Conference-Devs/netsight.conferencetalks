from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.dexterity.content import Item

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from netsight.conferencetalks import _

kwvocab = SimpleVocabulary.fromValues(('Tutorial',
                                       'New to Plone',
                                       'Developers',
                                       'Integrators',
                                       'Designers',
                                       'Enterprise',
                                       'Education',
                                       'Small Business',
                                       'Healthcare',
                                       'Government',
                                       'Case Study',
                                       ))

roomvocab = SimpleVocabulary.fromValues(('',
                                         'Wessex Suite',
                                         'Malborough Room',
                                         'Dutchess 1+2',
                                         'Dutchess 3+4',
                                         ))

dayvocab = SimpleVocabulary.fromValues(('',
                                        'Wednesday',
                                        'Thursday'))


times_wed = {0: ('2010/10/27 09:00', '2010/10/27 10:00'),
             1: ('2010/10/27 10:10', '2010/10/27 10:55'),
             2: ('2010/10/27 11:25', '2010/10/27 12:10'),
             3: ('2010/10/27 12:20', '2010/10/27 13:05'),
             4: ('2010/10/27 14:00', '2010/10/27 14:45'),
             5: ('2010/10/27 14:55', '2010/10/27 15:40'),
             6: ('2010/10/27 16:10', '2010/10/27 16:55'),
             7: ('2010/10/27 17:05', '2010/10/27 18:05'),
             }

times_thurs = {1: ('2010/10/28 09:00', '2010/10/28 09:45'),
               2: ('2010/10/28 09:55', '2010/10/28 10:40'),
               3: ('2010/10/28 11:10', '2010/10/28 11:55'),
               4: ('2010/10/28 12:05', '2010/10/28 12:50'),
               5: ('2010/10/28 14:00', '2010/10/28 14:45'),
               6: ('2010/10/28 14:55', '2010/10/28 15:40'),
               7: ('2010/10/28 16:10', '2010/10/28 16:55'),
               8: ('2010/10/28 17:05', '2010/10/28 18:05'),
               9: ('2010/10/28 18:15', '2010/10/28 18:55'),
               10: ('2010/10/28 19:00', '2010/10/28 23:55'),
               }

def calcTime(talk):

    day = talk.day
    slot = talk.slot
    if day == 'Wednesday':
        return times_wed[slot]
    elif day == 'Thursday':
        return times_thurs[slot]
    else:
        raise ValueError, 'Invalid day: %s' % day

class Talk(Item):
    def foo(self):
        """ foo """
        return "foo"

class ITalk(form.Schema):
    """A talk for the conference.
    """
    
    title = schema.TextLine(
            title=_(u"Title of the talk"),
            description=_(u"A short and precise title, 4-6 words"),
        )
    
    description = schema.Text(
            title=_(u"Description of the talk"),
            description=_(u"This should entice people to the talk and tell them what they will learn in this talk."),
        )

    detail = schema.Text(
        title=_(u"Detail of the talk"),
        )
    
    name = schema.TextLine(
        title=_(u"Name"),
        )

    
    company = schema.TextLine(
        title=_(u"Company / Organisation"),
        required=False,
        )

    email = schema.TextLine(
        title=_(u"Email Address"),
        )

    country = schema.TextLine(
        title=_(u"Country"),
        )

    bio = schema.Text(
            title=_(u"Short Biography"),
            description=_(u"Please give a short biography of yourself. Let people know what you do and why they should come hear your talk."),
        )

    portrait = NamedImage(
            title=_(u"Portrait"),
            description=_(u"Please upload a photo of yourself we can put on the website with your talk."),
            required=False,
        )

    requirements = schema.Text(
        title=_(u"Any other requirements"),
        required=False,
        )

    
    keywords = schema.List(
        title=_(u"Keywords"),
        value_type=schema.Choice(title=u"keywords", vocabulary=kwvocab),
        )

    dexterity.read_permission(votes='cmf.ReviewPortalContent')
    votes = schema.List(
        title=_(u"Votes"),
        value_type=schema.TextLine(title=u"vote"),
        required=False,
        )

    day = schema.Choice(
        title=_(u"Day"),
        vocabulary=dayvocab,
        )

    room = schema.Choice(
        title=_(u"Room"),
        vocabulary=roomvocab,
        )

    slot = schema.Int(
        title=_(u"Slot"),
        )

