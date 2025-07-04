# -*- coding: utf-8 -*-

# from medialog.newsletter import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class INewsLetterView(Interface):
    """ Marker Interface for INewsLetterView"""


class NewsLetterView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('news_letter_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.items = self.get_items()
        return self.index()
    
    def get_items(self):
        # TO DO, cache (?)
        # today = datetime.now()
        # could consider count from 'last month or similar'
        count = self.context.itemcount
        
        items = self.context.portal_catalog(
            portal_type=['News Item'],
            sort_on='effective',
            sort_order='descending'
        )[:count]
        
        if items:
            return items
        
        # No News Items found
        return None
        
