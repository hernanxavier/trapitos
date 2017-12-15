# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class tra_base(models.Model):
#     _name = 'tra_base.tra_base'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class tra_ColorTela (models.Model):
    _name = 'tra.color.tela'
    _description = 'Registra los colores posibles para las telas'
    _order = 'name'

    _sql_constraints = [
        ('unique_codigo','unique(codigo)', u'Otro color ya tiene este código'),
    ]
    name = fields.Char(u'Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 6, required = True)
    observacion = fields.Text (u'Observación', size = 200, required = False)


class tra_Tela(models.Model):
    _name = 'tra.tela'
    _description = u'Registra los valores básicos de la materia prima telas'
    _order = 'name'

    _sql_constraints = [
        ('unique_codigo', 'unique(codigo)', u'Otro tipo de tela ya tiene este código'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 100, required = True)
    ancho  = fields.Float('Ancho', size = 6, required = True)
    color_id = fields.Many2one('tra.color.tela', 'Color', required = True)
    costo = fields.Float('Costo', size = 6 , required = True)
    iva = fields.Float('IVA (%)', size =3 , required = True)
    observacion = fields.Char (u'Observación', size = 200, required = False)
