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
        return self.index()
