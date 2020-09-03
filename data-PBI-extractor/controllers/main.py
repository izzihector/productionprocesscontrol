import json
import random
import requests
from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools import date_utils
import json
import random
import requests

class PBIExport(CustomerPortal):
    #@http.route('/PBI/analytic/clientes/<string:user_id>', type="json", method=['POST','GET'], website=False, auth="public", csrf=False)

    @http.route(['/PBI/analytic/clientes'], type='http', auth="public", website=True)
    def get_tickets_analytic(self, access_token=None, report_type=None, download=False, **kw):
        #user_id = request.env['res.partner'].sudo().search([('name','=',kw.get('user_id'))])
        user = request.env['account.invoice'].sudo().search([('id','=','11')])
        raw_data = user.read()
        json_data = json.dumps(raw_data, default=date_utils.json_default)
        return json_data

