# -*- coding: utf-8 -*-
####################################################################
#
# © 2019-Today Somko Consulting (<https://www.somko.be>)
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/11.0/legal/licenses/licenses.html)
#
####################################################################
from collections import defaultdict

from odoo import models, api
from xml.etree.cElementTree import fromstring
import requests


class OocOoc(models.Model):
    _name = 'ooc.ooc'

    @api.model
    def is_installed(self):
        return True

    @api.model
    def create_mail(self, params):
        if len(params['attachments']) > 0:
            params['attachment_ids'] = [(6, 0, self.create_attachments(params))]

        del params['attachments']
        del params['ewsUrl']
        del params['token']
        del params['itemId']

        record = self.env['mail.message'].create(params)
        self.env['ooc.history'].sudo().create({'mail': record['id']})

        return record['id']

    @api.model
    def get_attachments(self, params):
        url = params['ewsUrl']
        headers = {'content-type': 'text/xml; charset=utf-8', 'Authorization': 'Bearer {0}'.format(params['token'])}
        body = """<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                   xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
                                   xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Header>
                        <t:RequestServerVersion Version="Exchange2007_SP1"/>
                    </soap:Header>
                    <soap:Body>
                        <m:GetItem>
                            <m:ItemShape>
                                <t:BaseShape>IdOnly</t:BaseShape>
                                <t:AdditionalProperties>
                                    <t:FieldURI FieldURI="item:Attachments"/>
                                </t:AdditionalProperties>
                            </m:ItemShape>
                            <m:ItemIds>
                                <t:ItemId Id="{0}"/>
                            </m:ItemIds>
                        </m:GetItem>
                    </soap:Body>
                </soap:Envelope>"""

        def etree_to_dict(t):
            d = {t.tag: {} if t.attrib else None}
            children = list(t)
            if children:
                dd = defaultdict(list)
                for dc in map(etree_to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                d = {t.tag: {k: v[0] if len(v) == 1 else v
                             for k, v in dd.items()}}
            if t.attrib:
                d[t.tag].update(('@' + k, v)
                                for k, v in t.attrib.items())
            if t.text:
                text = t.text.strip()
                if children or t.attrib:
                    if text:
                        d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text
            return d

        response = requests.post(url, data=body.format(params['itemId']), headers=headers, verify=False)
        xml = fromstring(response.content)
        xml_file_attachments = xml.find('.//t:Attachments', {'t': 'http://schemas.microsoft.com/exchange/services/2006/types'})
        dict_file_attachments = etree_to_dict(xml_file_attachments)

        return {
            file['{http://schemas.microsoft.com/exchange/services/2006/types}Name']: file['{http://schemas.microsoft.com/exchange/services/2006/types}AttachmentId']['@Id']
            for file in dict_file_attachments['{http://schemas.microsoft.com/exchange/services/2006/types}Attachments']['{http://schemas.microsoft.com/exchange/services/2006/types}FileAttachment']
        }

    @api.model
    def create_attachments(self, params):
        attachments = []

        if params['attachments']:
            ews_attachments = self.get_attachments(params)

            for att in params['attachments']:
                try:
                    content = self.get_attachment(params, ews_attachments[att['name']])
                    curr = Attachment(att['name'], content, params['model'], params['res_id'])
                    record = self.env['ir.attachment'].sudo().create(vars(curr))
                    attachments.append(record['id'])
                except:
                    pass

        return attachments

    @api.model
    def get_attachment(self, params, attachment_id):
        url = params['ewsUrl']
        headers = {'content-type': 'text/xml; charset=utf-8', 'Authorization': 'Bearer {0}'.format(params['token'])}
        body = """<?xml version="1.0" encoding="utf-8"?>
                       <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                           xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                           xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                           xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
                           <soap:Header>
                               <t:RequestServerVersion Version="Exchange2013" />
                           </soap:Header>
                           <soap:Body>
                               <GetAttachment xmlns="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
                                   <AttachmentShape/>
                                   <AttachmentIds>
                                       <t:AttachmentId Id="{0}"/>
                                   </AttachmentIds>
                               </GetAttachment>
                           </soap:Body>
                       </soap:Envelope>"""

        return self.soap_get_attachment_content(url, headers, body, attachment_id)

    @api.model
    def soap_get_attachment_content(self, url, headers, body, sid):
        response = requests.post(url, data=body.format(sid), headers=headers, verify=False)
        xml = fromstring(response.content)
        content = xml.find('.//t:Content', {'t': 'http://schemas.microsoft.com/exchange/services/2006/types'})

        return content.text


class Attachment(object):
    def __init__(self, name, content, res_model, res_id):
        self.name = name
        self.res_id = res_id
        self.res_model = res_model
        self.store_fname = name
        self.datas = content
        self.type = 'binary'
