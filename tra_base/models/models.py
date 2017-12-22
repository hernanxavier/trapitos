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
    @api.one
    def _get_costo_total (self):
        self.costo_total = self.costo + (self.costo*self.iva)/100

    _name = 'tra.tela'
    _description = u'Registra los valores básicos de la materia prima telas'
    _order = 'name'

    _sql_constraints = [
        ('unique_codigo', 'unique(codigo)', u'Otro tipo de tela ya tiene este código'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 100, required = True)
    ancho  = fields.Float('Ancho (m.)', size = 6, required = True)
    #color_id = fields.Many2one('tra.color.tela', 'Color', required = True)
    costo = fields.Float('Costo', size = 6 , required = True)
    iva = fields.Float('IVA (%)', size =3 , required = True)
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Costo Total')
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

class tra_Prenda(models.Model):
    _name = 'tra.prenda'
    _description = 'Registra el nombre de una prenda'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la prenda ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la prenda ya existe'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char('Codigo', size = 100, required = True)
    observacion = fields.Text(u'Observación', required = False)

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

class tra_Accesorio(models.Model):
    @api.one
    def _get_valor_total (self):
        #Calcula el campo largo total
        try:
            if self.iva and self.costo > 0:
                self.valor_total= ((self.costo * self.iva)/100) + self.costo
            else:
                self.valor_total = 0
        except:
            raise 'Datos incorrectos'

    _name = 'tra.accesorio'
    _description = 'Registra los materiales extras que tiene una prenda textil, asi como sus costos'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]

    name = fields.Char ('Nombre del material', size = 100, required = True)
    codigo = fields.Char (u'Código de producto', size = 9, required = True)
    costo = fields.Float ('Costo', size = 11, required = True)
    iva = fields.Float ('IVA(%)', size = 4, required = True)
    valor_total = fields.Float (compute = '_get_valor_total', string = 'Total')
    observacion = fields.Text ('Observaciones', required = False)

class tra_MateriaForro(models.Model):
    @api.one
    def _get_largo_total (self):
        # Calcula el campo largo total
        try:
            self.largo_total = self.largo_frente + self.largo_manga + self.scrap + self.largo_manga_extra
        except:
            raise 'Datos incorrectos'

    def _get_ancho_total (self):
        # Calcula el ancho total del Forro
        try:
            self.ancho_total = self.ancho_frente + self.ancho_espalda
        except:
            raise 'Datos incorrectos'

    def _get_piezas_reales (self):
        # Calcula el numero de piezas reales que salen de la tela escogida
        import math
        try:
            piezas = self.ancho_tela_id / self.ancho_total

            t = math.modf(piezas) # math.modf(Decimal) esto devuelve una tupla con la parte decimal y en la posicion 1 la parte entera
            if t[0] >= 0.50: # Si la aparte decimal es mayor a 0,50 entonces baja a 0,50
                piezas= t[1] + 0.50
            else: # Si es menor entonces solamente queda la parte entera
                piezas = t[1]

            self.piezas_reales = piezas
        except:
            raise 'Datos incorrectos'

    def _get_tela_utilizada (self):
        #Calcula la cantidad de tela utilizada para producir la prenda
        import math
        try:
            if self.piezas_reales > 0 :
                tela = math.ceil(1/self.piezas_reales)
                self.tela_utilizada = tela * self.largo_total
            else:
                self.tela_utilizada = 0
        except:
            raise 'Datos incorrectos'

    def _get_costo_tela_cuerpo (self):
        #Calcula el costo de tela utilizada en el cuerpo de la prenda
        import math
        try:
            if self.piezas_reales > 0 :
                costo = self.largo_total * self.costo_tela_id
                self.costo_tela_cuerpo = costo / self.piezas_reales
            else:
                self.costo_tela_cuerpo = 0
        except:
            raise 'Datos incorrectos'

    def _get_costo_tela_extra (self):
        # Calcula el costo de tela extra utilizada en la prenda
        import math
        try:
            self.costo_tela_extra = self.costo_tela_id * self.cantidad_tela_extra
        except:
            raise 'Datos incorrectos'

    def _get_costo_accesorios (self):
        # Suma el costo de los diferentes accesorios extras
        suma_costos = 0
        for costo in self.accesorio_ids:
            suma_costos += costo.valor_total
        self.costo_accesorios = suma_costos

    def _get_total_tela_utilizada (self):
        # Suma la cantidad de tela utilizada en el cuepro de laprenda y la cantidad extra
        self.total_tela_utilizada = self.tela_utilizada + self.cantidad_tela_extra

    def _get_costo_total(self):
        # Calcula el costo total de la tela utilizada para la prenta textil
        self.costo_total = self.costo_tela_extra + self.costo_tela_cuerpo + self.costo_accesorios

    _name = 'tra.materia.forro'
    _description = 'Registra el material que una prenda textil puede requerir'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        ('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]
    name = fields.Char('Nombre', required = True)
    codigo = fields.Char('Codigo de forro', required = True)
    tela_id = fields.Many2one ('tra.tela', 'Tela', required = True)
    talla_id = fields.Many2one ('tra.talla', 'Talla', required = True)
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

    #Campos relacionales
    ancho_tela_id = fields.Float('Ancho Tela', store = False, related = 'tela_id.ancho')
    costo_tela_id = fields.Float('Costo Tela', store = False, related = 'tela_id.costo')
    accesorio_ids = fields.Many2many('tra.accesorio', 'tra_forro_accesorio', 'forro_id', 'accesorio_id', string = 'Accesorios Extra')

    # Campos Calculados
    largo_total = fields.Float(compute = '_get_largo_total', string = 'Largo Total')
    ancho_total = fields.Float(compute = '_get_ancho_total', string = 'Ancho Total')
    piezas_reales = fields.Float(compute = '_get_piezas_reales', string = 'Nro. Piezas')
    tela_utilizada = fields.Float(compute = '_get_tela_utilizada', string = 'Tela Utilizada (Cuerpo)')
    costo_tela_cuerpo = fields.Float(compute = '_get_costo_tela_cuerpo', string = 'Costo Tela')
    costo_tela_extra = fields.Float(compute = '_get_costo_tela_extra', string = 'Costo Tela Extra')
    costo_accesorios = fields.Float(compute = '_get_costo_accesorios', string = 'Costo Accesorios Extras')
    total_tela_utilizada = fields.Float(compute = '_get_total_tela_utilizada', string = 'Total Tela Utilizada (Cuerpo + Extra)')
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Costo Total')



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
