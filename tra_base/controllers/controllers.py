# -*- coding: utf-8 -*-
from odoo import http

# class TraBase(http.Controller):
#     @http.route('/tra_base/tra_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tra_base/tra_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tra_base.listing', {
#             'root': '/tra_base/tra_base',
#             'objects': http.request.env['tra_base.tra_base'].search([]),
#         })

#     @http.route('/tra_base/tra_base/objects/<model("tra_base.tra_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tra_base.object', {
#             'object': obj
#         })