# -*- coding: utf-8 -*-

# from medialog.newsletter import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from Products.CMFPlone.interfaces import IMailSchema
from zope.component import adapter, getUtility
from plone.registry.interfaces import IRegistry
from zope.interface.interfaces import ComponentLookupError
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

from Products.statusmessages.interfaces import IStatusMessage
from Products.statusmessages.interfaces import IStatusMessage
from medialog.newsletter import _

from  medialog.newsletter.views.news_letter_view import NewsLetterView
from Products.CMFPlone import PloneMessageFactory as _

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
# from plone.app.layout.viewlets.common import ViewletBase


class ISendNewsLetterView(Interface):
    """ Marker Interface for ISendNewsLetterView"""


class SendNewsLetterView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('send_news_letter_view.pt')
    

    def __call__(self):
        request = self.request
        if 'groupmail' in request.form:
            self.send_groupmail()
        else:
            self.send_testmail() 
        return self.index()

    def send_groupmail(self):
        context = self.context
        request = self.request
        # To do: get users from somewhere
        # Currently, it is sending to 'everybody/all_users'
        if hasattr(context, 'group'):
            group = context.group
            usergroup = api.user.get_users(groupname=group)
        else:
            usergroup = api.user.get_users()

        for member in usergroup:
            group = api.group.get_groups(user=member)
            receipt = member.getProperty('email')
            self.send_email(context, request, receipt)

        self.request.response.redirect(self.context.absolute_url())
        

    def more_message(self):
        items = NewsLetterView.get_items(self)
        if not items:
            return ''

        html_output = ''
        for item in items:
            obj = item.getObject()
            scales = getMultiAdapter((obj, self.request), name="images")
            thumbnail = scales.scale('image', width=600)

            image_html = ''
            if thumbnail:
                image_html = f"""
                <div style="padding: 0; margin: 0.5rem 0">
                    <figure>
                        <img style="margin: 1rem0 0.5rem" 
                             src="{thumbnail.url}" width="{thumbnail.width}" height="{thumbnail.height}" loading="lazy"/>
                        <figcaption style="color: #777;">{obj.image_caption or ''}</figcaption>
                    </figure>
                </div>
                """

            html_output += f"""
            <article>
                {image_html}
                <a href="{item.getURL()}" style="text-decoration: none">
                    <h3 style="color: #123456">{item.Title}</h3>
                </a>
                <p style="font-weight:bold; font-size: 16px">{item.Description}</p>
                <div>{obj.text.output if obj.text else ''}</div>
                
                <a style="color: #fff; background-color: #0dcaf0; 
                    border: 1px solid #0dcaf0; padding: 0.375rem 0.75rem; 
                    font-size: 1rem; line-height: 1.5; 
                    border-radius: 0.375rem;
                    href="{item.getURL()}">Read More …</a>
            </article>
            <div style="padding: 2rem; margin: 2rem;"><hr/></div>
            """

        return html_output


    def send_email(self, context, request, receipt):        
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        #interpolator = IStringInterpolator(obj)

        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            abc = 1
            raise ComponentLookupError(
                "You must have a Mailhost utility to \
            execute this action"
            )

        self.email_charset = self.mail_settings.email_charset
        
        title = context.Title()
        description = context.Description()
        ## To do, get all content here
        # body_html =  u'<html><div class="mailcontent" style="width:600px"><h1 class="documentFirstHeading">\
        #     ' + title  + u'</h1><div class="documentDescription description">' + description  + u'</div>' + context.text.output 
        #for 'non HTML mail clients'
        # transforms = api.portal.get_tool(name='portal_transforms')
        # stream = transforms.convertTo('text/plain', body_html, mimetype='text/html')
        # body_plain = stream.getData().strip()

        messages = IStatusMessage(self.request)

        # ready to create multipart mail
        try:
            message =  f"""<html>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                
                <div style="max-width: 600px; margin: 20px auto; 
                background-color: #ffffff; padding: 20px; 
                font-size: 15px; line-height: 1.6; color: #333;">    
                <img src="http://ubuntu.local:8605/Plone19/++resource++plone-logo.svg" alt="Plone logo"/>  
                Our logo
                <h1 style="color: #123456; font-size: 24px; margin-top: 0;">
                {title}</h1>
                 <div style="font-style: italic; color: #555; margin-bottom: 20px; font-size: 20px">
                {description}
                </div>
                {context.text.output}
                <div style="padding: 2rem; margin: 2rem;"><hr/></div>
                """
            message += self.more_message() 
            message +=  u'</div></html>'
            outer = MIMEMultipart('alternative')
            outer['To'] = receipt
            # outer['From'] = api.portal.get_registry_record('plone.email_from_address')
            outer['From'] = self.mail_settings.email_from_address 
            outer['Subject'] =  title                    
            outer.epilogue = ''

            # Attach text part
            html_part = MIMEMultipart('related')
            html_text = MIMEText(message, 'html', _charset='UTF-8')
            html_part.attach(html_text)
            outer.attach(html_part)
            mailhost.send(outer.as_string())
                    
            # # Finally send mail.
            mailhost.send(outer.as_string())                         

            messages.add(_("sent_mail_message",  default=u"Sent to  $email",
                                                 mapping={'email': receipt },
                                                 ),
                                                 type="info")

        except:
            messages.add(_("cant_send_mail_message",
                                                 default=u"Could not send to $email",
                                                 mapping={'email': receipt },
                                                 ),
                                                 type="warning")


    def send_testmail(self):
        context = self.context
        request = self.request
        member = api.user.get_current()
        receipt = member.getProperty('email')
        if receipt:
            self.send_email(context, request, receipt)
        else:
            messages = IStatusMessage(self.request)
            messages.add(_("cant_send_mail_message",
                                                 default=u"User does not have email",
                                                 mapping={'email': receipt },
                                                 ),
                                                 type="error")
            
        self.request.response.redirect(self.context.absolute_url())