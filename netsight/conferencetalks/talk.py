from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.dexterity.content import Item

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from netsight.conferencetalks import _

kwvocab = SimpleVocabulary.fromValues((u'Tutorial',
                                       u'New to Plone',
                                       u'Developers',
                                       u'Integrators',
                                       u'Designers',
                                       u'Enterprise',
                                       u'Education',
                                       u'Small Business',
                                       u'Healthcare',
                                       u'Government',
                                       u'Case Study',
                                       u'Related Technologies',
                                       ))

# room code names. Easier than numbers. cali microbrews
roomvocab = SimpleVocabulary.fromValues(('',
                                         u'Stone',
                                         u'Pyramid',
                                         u'Anchor',
                                         u'Green Flash',
                                         u'AleSmith',
                                         u'Biersch',
                                         u'Strauss',
                                         u'Ballast',
                                         u'Firestone',
                                         ))

dayvocab = SimpleVocabulary.fromValues((u'',
                                        u'Wednesday',
                                        u'Thursday',
                                        u'Friday',
                                        u'Saturday',
                                        u'Sunday'))
                                        
talklengthvocab = SimpleVocabulary.fromValues(("I'm not sure - squeeze me in where it makes sense",
                                                '30 minutes',
                                                '45 minutes'))


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
    if not (slot and day):
        return None
        
    # what does this do...?
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
        
    talklength = schema.Choice(
        title=_(u"Talk Length"),
        vocabulary=talklengthvocab,
        required=False,
    )
    
    audience = schema.Text(
            title=_(u"Who is the target audience for this talk?"),
            description=_(u"Please be detailed so we can put you in the right room."),
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
        required=False,
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
        required=False,
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
        required=False,
        )

    room = schema.Choice(
        title=_(u"Room"),
        vocabulary=roomvocab,
        required=False,
        )

    slot = schema.Int(
        title=_(u"Slot"),
        required=False,
        )

