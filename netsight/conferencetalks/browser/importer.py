from Products.Five import BrowserView
import gdata.spreadsheet.service
from plone.dexterity.utils import createContentInContainer
from zope.app.container.interfaces import INameChooser
import csv
from Products.CMFCore.utils import getToolByName


def utf_8_encoder(csv_data):
    for line in csv_data:
        yield unicode(line, errors='replace').encode('ascii', 'replace')


class importer(BrowserView):

    def __call__(self):
        self.twentyeleven()
    
    def twentyeleven(self):
        workflowTool = getToolByName(self.context, "portal_workflow")
        with open("data/talks.csv") as csvFile:
            csvData = csvFile.readlines()
            reader = csv.DictReader(utf_8_encoder(csvData), delimiter=',')
            for row in reader:
                name = row['Your Name']
                title = row['Title of Talk']
                description = row['Summary of Talk']
                detail = row['Talk Outline']
                talklength = row['Talk Length']
                audience = row['Intended Audience']
                bio = row['Speaker Bio']
                email = row['Your Email']
                talks = self.context
                talk = createContentInContainer(talks, 'netsight.conferencetalks.talk',
                                                checkConstraints=False,
                                                title=title,
                                                description=description,
                                                detail=detail,
                                                name=name,
                                                company='',
                                                email=email,
                                                country='',
                                                bio=bio,
                                                talklength = talklength,
                                                audience = audience,
                                                requirements='',
                                                keywords=[],
                                                )
                workflowTool.doActionFor(talk, "publish")
                                    
        
    def twentyten(self):

        gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gd_client.email = 'ploneconf@gmail.com'
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
