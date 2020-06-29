from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class PBIExport(CustomerPortal):
    @http.route(['/PBI/analytic/tickets'], type='http', auth="public", website=True)
    def get_tickets_analytic(self, access_token=None, report_type=None, download=False, **kw):
        return "SI"