# -*- coding: utf-8 -*-

from medialog.newsletter import _
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations
from Products.Five.browser import BrowserView
from persistent.list import PersistentList
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

SUBSCRIBERS_KEY = 'medialog.newsletter.subscribers'

class IManageSubscribersView(Interface):
    """ Marker Interface for IManageSubscribersView"""

 

class ManageSubscribersView(BrowserView):
    template = ViewPageTemplateFile('manage_subscribers.pt')

    def __call__(self):
        if 'form.subscribed' in self.request.form:
            return self._handle_add()
        elif 'form.unsubscribe' in self.request.form:
            return self._handle_remove()
        return self.template()  # Calls template, avoids recursion

    def _get_storage(self):
        annotations = IAnnotations(self.context)
        if SUBSCRIBERS_KEY not in annotations:
            annotations[SUBSCRIBERS_KEY] = PersistentList()
        return annotations[SUBSCRIBERS_KEY]

    def _handle_add(self):
        email = self.request.form.get('email', '').strip().lower()
        messages = IStatusMessage(self.request)
        if email:
            storage = self._get_storage()
            if email not in storage:
                storage.append(email)
                messages.add("Successfully subscribed.", type="info")
            else:
                messages.add("Already subscribed.", type="warning")
        else:
            messages.add("Email is required.", type="error")
        return self.request.response.redirect(self.context.absolute_url() + '/@@manage-subscribers')

    def _handle_remove(self):
        email = self.request.form.get('email', '').strip().lower()
        messages = IStatusMessage(self.request)
        storage = self._get_storage()
        if email and email in storage:
            storage.remove(email)
            messages.add("Unsubscribed successfully.", type="info")
        else:
            messages.add("Email not found or invalid.", type="warning")
        return self.request.response.redirect(self.context.absolute_url() + '/@@manage-subscribers')

    def subscribers(self):
        return sorted(self._get_storage())