# -*- coding: utf-8 -*-
from odoo import http

# class TraCostos(http.Controller):
#     @http.route('/tra_costos/tra_costos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tra_costos/tra_costos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tra_costos.listing', {
#             'root': '/tra_costos/tra_costos',
#             'objects': http.request.env['tra_costos.tra_costos'].search([]),
#         })

#     @http.route('/tra_costos/tra_costos/objects/<model("tra_costos.tra_costos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tra_costos.object', {
#             'object': obj
#         })