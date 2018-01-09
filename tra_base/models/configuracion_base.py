# -*- coding: utf-8 -*-

# from odoo import fields, models, api
#
#
# class tra_GastoVentaConfiguracion(models.TransientModel):
#     # @api.one
#     # @api.depends('default_gastos_ventas', 'default_gastos_viajes', 'default_gastos_operacion', 'default_gastos_varios', 'default_servicios_basicos')
#     # def _get_total_gastos_venta(self):
#     #     self.default_total_gastos_venta = self.default_gastos_ventas + self.default_gastos_viajes + self.default_gastos_varios + self.default_gastos_operacion + self.default_servicios_basicos
#     #
#     # @api.one
#     # @api.depends('default_total_gastos_venta','default_venta_anual')
#     # def _get_tasa_costo_ventas(self):
#     #     if self.default_venta_anual > 0:
#     #         self.default_tasa_costo_ventas = self.default_total_gastos_venta / self.default_venta_anual
#
#     _inherit = 'res.config.settings'
#     _name = 'tra.gasto.venta'
#     _description = 'Registra y calcula valores de gastos de venta'
#
#     default_fecha = fields.Date('Fecha', required = True)
#     default_gastos_ventas = fields.Float ('Gastos de Ventas', size = 11, required = True)
#     default_gastos_viajes = fields.Float ('Gastos de Viajes', size = 11, required = True)
#     default_gastos_operacion = fields.Float ('Gastos Operacionales', size = 11, required = True)
#     default_gastos_varios = fields.Float ('Gastos Varios', size = 11, required = True)
#     default_servicios_basicos = fields.Float (u'Servicios Básicos', size = 11, required = True)
#     default_venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
#     default_observacion = fields.Text ('Observaciones', required = False)
#
#     # #Campos Calculados
#     # default_total_gastos_venta = fields.Float(compute = '_get_total_gastos_venta', string = 'Total Gastos Venta', store = True)
#     # default_tasa_costo_ventas = fields.Float(compute = '_get_tasa_costo_ventas', string = 'Tasa Costo de Ventas', store = True)
