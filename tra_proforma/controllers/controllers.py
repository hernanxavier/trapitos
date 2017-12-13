# -*- coding: utf-8 -*-
from odoo import http

# class TraProforma(http.Controller):
#     @http.route('/tra_proforma/tra_proforma/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tra_proforma/tra_proforma/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tra_proforma.listing', {
#             'root': '/tra_proforma/tra_proforma',
#             'objects': http.request.env['tra_proforma.tra_proforma'].search([]),
#         })

#     @http.route('/tra_proforma/tra_proforma/objects/<model("tra_proforma.tra_proforma"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tra_proforma.object', {
#             'object': obj
#         })