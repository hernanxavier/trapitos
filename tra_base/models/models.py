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

class tra_ManoObraDirecta(models.Model):
    # Agrega campos al modulo de empleados
    _inherit = 'hr.employee'
    sueldo_fijo = fields.Float('Sueldo Mensual ($)')
    valor_iess = fields.Float('Aprote al IESS (%)')
    valor_horas_extra = fields.Float ('Horas Extras ($)')
    valor_bonos = fields.Float('Premios/Incentivos ($)')
    costo_minuto_mod = fields.Float ('Costo M.O. Directa ($)')
    proyeccion_incremento = fields.Float (u'Proyección Incremento')


class tra_ColorTela (models.Model):
    _name = 'tra.color.tela'
    _description = 'Registra los colores posibles para las telas'
    _order = 'name'

    _sql_constraints = [
        ('unique_codigo','unique(codigo)', u'Otro color ya tiene este código'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 6, required = True)
    observacion = fields.Text (u'Observación', required = False)


class tra_Tela(models.Model):
    _name = 'tra.tela'
    _description = u'Registra los valores básicos de la materia prima telas'
    _order = 'name'

    _sql_constraints = [
        ('unique_codigo', 'unique(codigo)', u'Otro tipo de tela ya tiene este código'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 100, required = True)
    ancho  = fields.Float('Ancho (m.)', size = 6, required = True)
    color_id = fields.Many2one('tra.color.tela', 'Color', required = True)
    costo = fields.Float('Costo', size = 6 , required = True)
    iva = fields.Float('IVA (%)', size =3 , required = True)
    observacion = fields.Text ('Observación', required = False)

class tra_Talla(models.Model):
    _name = 'tra.talla'
    _description = 'Registra las tallas posibles de una prenda'
    _order = 'name'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'Esta talla ya existe'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    observacion = fields.Text('Observaciones', size = 200 , required = False)

class tra_TiempoTrabajo(models.Model):
    _name = 'tra.tiempo.trabajo'
    _description = 'Registra el tiempo de descanso y dias laborables de una jornada laboral'
    _order = 'name'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]
    name = fields.Char('Nombre Jornada', size = 100, required = True)
    codigo = fields.Char (u'Código', size = 3, required = True)
    jornada_horas = fields.Float ('Horas Laborales', size = 10, required = True)
    descanso_horas = fields.Float('Horas de descanso', size = 10, required = True)
    dia_laborables_anio = fields.Float(u'Dias laborables (Año)', size = 3, required = True)
    observacion = fields.Text('Observacion', required = False)

class tra_FormaPago(models.Model):
    _name = 'tra.forma.pago'
    _description = 'Registra las diferentes formas de pago para los clientes'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char ('Nombre', size = 6, required = True)
    recargo = fields.Float('Regargo', size = 9, required = True)
    observacion = fields.Text(u'Observación', required = False)

class tra_Utilidad(models.Model):
    _name = 'tra.utilidad'
    _description = 'Registra valores de utilidades aplicadas de acuerdo a las unidades compradas o a la forma de pago'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char('Codigo', size = 6, required = True)
    num_unidades = fields.Float('Num. Unidades', size = 6, required = True)
    porcentaje = fields.Float('Porcentaje Utilidad', size = 3, required = True)
    observacion = fields.Text (u'Observación', required = False)

class tra_MateriaExtra(models.Model):
    _name = 'tra.materia.extra'
    _description = 'Registra los materiales extras que tiene una prenda textil, asi como sus costos'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]

    name = fields.Char ('Nombre del material', size = 100, required = True)
    codigo = fields.Char (u'Código de producto', size = 9, required = True)
    costo = fields.Float ('Costo', size = 11, required = True)
    iva = fields.Float ('IVA(%)', size = 4, required = True)
    valor_total = fields.Float ('Total', size = 9, required = True)
    observacion = fields.Text ('Observaciones', required = False)

class tra_MateriaForro(models.Model):
    _name = 'tra.materia.forro'
    _description = 'Registra el material que una prenda textil puede requerir'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]

    name = fields.Char('Nombre', required = True)
    codigo = fields.Char('Codigo de forro', required = True)
    tela_id = fields.Many2one ('tra.tela', 'Tela', required = True)
    largo_frente = fields.Float ('Largo de Frente', size = 6, required = True)
    ancho_frente = fields.Float ('Ancho de Frente', size = 6, required = True)
    largo_espalda = fields.Float ('Largo de Espalda', size = 6, required = True)
    ancho_espalda = fields.Float ('Ancho de Espalda', size = 6, required = True)
    largo_manga = fields.Float ('Largo de Manga', size = 6, required = True)
    ancho_manga = fields.Float ('Ancho de Manga', size = 6, required = True)
    scrap = fields.Float ('SCRAP', size = 6, required = True)
    largo_manga_extra = fields.Float ('Largo de Manga Extra', size = 6, required = True)
    cantidad_tela_extra = fields.Float ('Cantidad de tela extra', size = 6, required = True)
    observacion = fields.Text ('Observaciones', required = False)

class tra_GastoVenta(models.Model):
    _name = 'tra.gasto.venta'
    _description = 'Registra y calcula valores de gastos de venta'

    fecha = fields.Date('Fecha', required = True)
    gastos_ventas = fields.Float ('Gastos de Ventas', size = 11, required = True)
    gastos_viajes = fields.Float ('Gastos de Viajes', size = 11, required = True)
    gastos_operacion = fields.Float ('Gastos Operacionales', size = 11, required = True)
    gastos_varios = fields.Float ('Gastos Varios', size = 11, required = True)
    servicios_basicos = fields.Float (u'Servicios Básicos', size = 11, required = True)
    venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
    observacion = fields.Text ('Observaciones', required = False)

class tra_GastoAdmin(models.Model):
    _name = 'tra.gasto.admin'
    _description = 'Registra y calcula valores de gastos administrativos'

    fecha = fields.Date('Fecha', required = True)
    gastos_admin = fields.Float ('Gastos de Administrativos', size = 11, required = True)
    gastos_operacion = fields.Float ('Gastos Operacionales', size = 11, required = True)
    gastos_varios = fields.Float ('Gastos Varios', size = 11, required = True)
    mantenimiento = fields.Float (u'Mantenimiento', size = 11, required = True)
    egresos_no_operativos = fields.Float(u'Gastos no operativos')
    venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
    observacion = fields.Text ('Observaciones', required = False)

class tra_GastoIndFabricacion(models.Model):
    _name = 'tra.gasto.ind.fabricacion'
    _description = 'Registra y calcula valores de gastos indirectos de fabricacion'

    fecha = fields.Date('Fecha', required = True)
    gastos_produccion = fields.Float (u'Gastos de producción', size = 11, required = True)
    servicios_basicos = fields.Float (u'Servicios básicos', size = 11, required = True)
    mano_obra_indirecta = fields.Float (u'Mano de obra indirecta', size = 11, required = True)
    venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
    observacion = fields.Text ('Observaciones', required = False)
