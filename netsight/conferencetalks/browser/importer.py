from Products.Five import BrowserView
import gdata.spreadsheet.service
from plone.dexterity.utils import createContentInContainer
from zope.app.container.interfaces import INameChooser


class importer(BrowserView):

    def __call__(self):

        gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gd_client.email = 'matth@netsight.co.uk'
        gd_client.password = 'secret'
        gd_client.source = 'myscript'
        gd_client.ProgrammaticLogin()
        key = 'tI6PI48mSIg-ZwiELfHe5Ww'
        worksheet = 'od6'
        feed = gd_client.GetListFeed(key, worksheet)
        for entry in feed.entry:
            data = entry.custom
            title = data['titleofyourproposedsession'].text
            description = data['abrief1-2paragraphdescriptionofyoursessionsuitableforpublishingintheconferenceprogram.'].text
            detail = data['describeyoursessionfullyaslongasyouneedforthebenefitoftheconferenceprogramcommittee.'].text
            name = data['name'].text
            company = data['organisationcompany'].text
            email = data['emailaddress'].text
            country = data['country'].text
            bio = data['tellusalittleaboutyourselfandwhyyoullbeanengaginginformativesessionleader.'].text
            requirements = data['anyothercommentsrequirements'].text
            keywords = data['sessionkeywords'].text.split(',')

            
            talks = self.context


            talk = createContentInContainer(talks, 'netsight.conferencetalks.talk',
                                            checkConstraints=False,
                                            title=title,
                                            description=description,
                                            detail=detail,
                                            name=name,
                                            company=company,
                                            email=email,
                                            country=country,
                                            bio=bio,
                                            requirements=requirements,
                                            keywords=keywords
                                            )

        return feed.entry[0].custom['name'].text
