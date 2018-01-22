# -*- coding: utf-8 -*-
from odoo import models, fields, api

class tra_CostesManoObraDirecta(models.Model):
    # Extrae del Modelo Tiempo Trabajo para el valor por defecto de jornada_laboral_id
    @api.multi
    @api.onchange ('tasa_empleado')
    def _get_jornada_laboral(self):
        for i in self:
            i.jornada_laboral_id = i.env['tra.tiempo.trabajo'].search([], limit = 1).id

    # Agrega campos al modulo de empleados
    _inherit = 'hr.employee'
    sueldo_fijo = fields.Float('Sueldo Anual: ($)')
    valor_iess = fields.Float('Aprote IESS ($)')
    valor_horas_extra = fields.Float ('Horas Extras: ($)')
    valor_bonos = fields.Float('Bonos ($)')
    jornada_laboral_id = fields.Many2one('tra.tiempo.trabajo', 'Jornada', default = _get_jornada_laboral)
    minutos_anual = fields.Float('Minutos', related = 'jornada_laboral_id.minutos_persona_anual', store = False)
    # Campos calculados
    total_sueldo_fijo = fields.Float(compute = '_get_total_sueldo_fijo',  store = True, string = 'Total Sueldo Fijo')
    total_sueldo_variable = fields.Float (compute = '_get_total_sueldo_variable', store = True, string = 'Total Sueldo Variable')
    total_sueldo = fields.Float(compute = '_get_total_sueldo', store = True, string = 'Total Sueldo')
    tasa_empleado = fields.Float (compute = '_get_tasa_empleado', digits = (3,4), string = 'Tasa')

    @api.multi
    @api.depends('sueldo_fijo', 'valor_iess')
    def _get_total_sueldo_fijo(self):
        for i in self:
            i.total_sueldo_fijo = i.sueldo_fijo + i.valor_iess

    @api.multi
    @api.depends('valor_horas_extra', 'valor_bonos')
    def _get_total_sueldo_variable(self):
        for i in self:
            i.total_sueldo_variable = i.valor_horas_extra + i.valor_bonos

    @api.multi
    @api.depends('total_sueldo_fijo', 'total_sueldo_variable')
    def _get_total_sueldo(self):
        for i in self:
            i.total_sueldo = i.total_sueldo_fijo + i.total_sueldo_variable

    @api.multi
    @api.onchange('total_sueldo','minutos_anual')
    @api.depends('total_sueldo','minutos_anual')
    def _get_tasa_empleado (self):
        for i in self:
            if i.minutos_anual > 0:
                i.tasa_empleado = i.total_sueldo / i.minutos_anual


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
    # No puede repetirse ni nombre ni código
    _sql_constraints = [
        ('unique_name', 'unique(name)', u'Otro tipo de tela ya tiene este NOMBRE'),
        ('unique_codigo', 'unique(codigo)', u'Otro tipo de tela ya tiene este CÓDIGO'),
    ]

    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 10, required = True)
    ancho  = fields.Float('Ancho (m.)', size = 6, required = True)
    costo = fields.Float('Costo', size = 6 , required = True)
    iva = fields.Float('IVA (%)', size =3 , required = True)
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Costo Total', store = True)
    observacion = fields.Text ('Observación', required = False)

    @api.multi
    @api.depends('costo', 'iva')
    @api.onchange('costo', 'iva')
    def _get_costo_total (self):
        # Calcula costo total por metro de tela
        for i in self:
            i.costo_total = i.costo + ((i.costo * i.iva)/100)

    @api.multi
    @api.onchange('name')
    def _get_uppercase_nombre(self):
        # Cambia a mayúsculas el nombre
        for i in self:
            if i.name != False:
                i.name = i.name.upper()

    @api.multi
    @api.onchange('name')
    def _get_codigo(self):
        # Genera el código de una tela registrada con las primeras letras de cada palabra en el nombre
        nombre = cod = ''
        for i in self:
            if i.name != False:
                i.name = i.name.strip()
                nombre = i.name.split(' ')
                for palabra in nombre:
                    cod += palabra[0].upper()
                i.codigo = cod

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
    # _name = 'tra.prenda'
    _description = 'Registra el nombre de una prenda'
    _order = 'name'
    _inherit = 'product.template'

    _sql_constraints = [
        #('unique_codigo', 'unique(codigo)', 'Otra prenda tiene el mismo código. Por favor escriba otro código'),
        #('unique_name_tela_talla', 'unique(name, tela_id, talla_id)', 'La prenda ya existe. Escriba otro nombre, tela o talla'),
    ]

    #name = fields.Char('Nombre', size = 100, required = True)
    tela_id = fields.Many2one ('tra.tela', 'Tela', required = True)
    talla_id = fields.Many2one ('tra.talla', 'Talla', required = True)
    forro_id = fields.Many2one ('tra.materia.forro', 'Forro', required = False)

    @api.multi
    @api.onchange('talla_id')
    def _get_codigo_prenda(self):
        # Agrega la T+talla al nombre y genera un codigo para la prenda
        nombre = cod = ''
        for i in self:
            if i.name and i.talla_id.name != False:
                i.name = i.name.strip()
                nombre = i.name.split(' ')
                for palabra in nombre:
                    cod += palabra[0].upper()
                i.default_code = cod + '0T' + i.talla_id.name
                i.name += ' T' + i.talla_id.name

    @api.multi
    @api.onchange('name')
    def _get_uppercase_nombre(self):
        # Convierte el texto de Nombre en mayúsculas
        for i in self:
            if i.name != False:
                i.name = i.name.upper()


class tra_TiempoTrabajo(models.Model):
    _name = 'tra.tiempo.trabajo'
    _description = 'Registra el tiempo de descanso y dias laborables de una jornada laboral'

    name = fields.Char('Nombre Jornada', size = 100, required = True)
    jornada_horas = fields.Float ('Horas Laborales', size = 3, required = True)
    descanso_minutos = fields.Float('Minutos de descanso (Día)', size = 3, required = True)
    dia_laborables_anio = fields.Float(u'Dias laborables (Año)', size = 3, required = True)
    minutos_producidos_anio = fields.Float('Minutos Producidos(Año)', size = 9, required = True)
    proyeccion_incremento = fields.Float ('Proyeccion de Incremento(%)', size = 4, requiered = True)
    observacion = fields.Text('Observacion', required = False)

    #Campos calculados
    jornada_diaria_min = fields.Float(compute = '_get_jornada_diaria_min', string = 'Joranada diaria (min.)', store = True)
    minutos_persona_anual = fields.Float(compute = '_get_minutos_persona_anual', string = 'Minutos persona laborados (año)', store = True)

    @api.multi
    @api.depends('jornada_horas', 'descanso_minutos')
    def _get_jornada_diaria_min (self):
        for diaria in self:
            diaria.jornada_diaria_min = (diaria.jornada_horas * 60) - diaria.descanso_minutos

    @api.multi
    @api.depends('jornada_diaria_min', 'dia_laborables_anio')
    def _get_minutos_persona_anual(self):
        for minutos in self:
            minutos.minutos_persona_anual = minutos.jornada_diaria_min * minutos.dia_laborables_anio

class tra_ManoObraDirecta(models.Model):
    @api.multi
    @api.depends('personal_ids', 'observacion')
    @api.onchange('personal_ids', 'observacion')
    def _get_jornada_laboral(self):
        for i in self:
            i.tiempo_trabajo_id = i.env['tra.tiempo.trabajo'].search([], limit = 1).id


    _name = 'tra.mano.obra.directa'
    _description = 'Registra y calcula el valor de la mano de Obra en la empresa'

    name = fields.Char('Nombre', size = 100)
    tiempo_trabajo_id = fields.Many2one('tra.tiempo.trabajo', 'Jornada', default = _get_jornada_laboral, store = True )
    jornada_diaria_min_id =fields.Float('Minutos Jornada Diaria', store = False, related = 'tiempo_trabajo_id.jornada_diaria_min')
    dia_laborables_anio_id = fields.Float('Días Laborables Anual', store = False, related = 'tiempo_trabajo_id.dia_laborables_anio')
    minutos_persona_anual_id = fields.Float('Minutos por Persona Anual', store = False, related = 'tiempo_trabajo_id.minutos_persona_anual')
    minutos_producidos_anio_id = fields.Float('Minutos Producidos Año', store = False, related = 'tiempo_trabajo_id.minutos_producidos_anio')
    proyeccion_incremento_id = fields.Float('Proyección de incremento (%)', store = False, related = 'tiempo_trabajo_id.proyeccion_incremento')
    observacion = fields.Text('Observaciones', required = False)
    #Campos realcionales
    personal_ids = fields.Many2many('hr.employee', 'tra_mod_employee', 'mod_id','employee_id', string = 'Lista empleados')
    #Campos calculados
    numero_personal = fields.Float(compute = '_get_numero_personal', string = 'Número de empleados', store = True )
    suma_total_sueldo_fijo = fields.Float(compute = '_get_suma_total_sueldo_fijo', string = 'Suma Sueldos Fijos', store = True )
    suma_total_sueldo_variable = fields.Float(compute = '_get_suma_total_sueldo_variable', string = 'Suma Sueldos Variables', store = True)
    suma_sueldos = fields.Float(compute = '_get_suma_sueldos', string = 'Costo Total MOD', store = True)
    suma_tasas = fields.Float(compute = '_get_suma_tasas', string = 'Suma de Tasas', digits = (3,4), store = True)
    tasa_parcial = fields.Float(compute = '_get_tasa_parcial', string = 'Tasa Parcial', digits = (3,4), store = True)
    costo_minuto_mod = fields.Float(compute = '_get_costo_minuto_mod', string = 'Costo Minuto MOD', digits = (3,4), strore = True)
    tasa_final = fields.Float(compute = '_get_tasa_final', string = 'Tasa Final', digits = (3,4), store = True)
    #tasa_final = fields.Float('Tasa Final')

    @api.multi
    @api.depends('personal_ids')
    @api.onchange('personal_ids')
    def _get_numero_personal(self):
        # Cuenta el número de empleados asignados
        contador = 0
        for i in self:
            for persona in i.personal_ids:
                contador += 1
            i.numero_personal = contador

    @api.multi
    @api.depends ('personal_ids')
    def _get_suma_total_sueldo_fijo (self):
        suma = 0
        for i in self:
            for persona in i.personal_ids:
                suma += persona.total_sueldo_fijo
            i.suma_total_sueldo_fijo = suma

    @api.multi
    @api.depends ('personal_ids')
    def _get_suma_total_sueldo_variable (self):
        suma = 0
        for i in self:
            for persona in i.personal_ids:
                suma += persona.total_sueldo_variable
            i.suma_total_sueldo_variable = suma

    @api.multi
    @api.depends('suma_total_sueldo_fijo','suma_total_sueldo_variable')
    def _get_suma_sueldos(self):
        for i in self:
            i.suma_sueldos = i.suma_total_sueldo_fijo + i.suma_total_sueldo_variable

    @api.multi
    @api.depends ('personal_ids')
    def _get_suma_tasas (self):
        suma = 0
        for i in self:
            for persona in i.personal_ids:
                suma += persona.tasa_empleado
            i.suma_tasas = suma

    @api.multi
    @api.depends ('suma_tasas')
    @api.onchange ('suma_tasas')
    def _get_tasa_parcial(self):
        for i in self:
            print ('Aquiiiiiii', i.numero_personal, i.suma_tasas)
            if i.numero_personal > 0 :
                i.tasa_parcial = i.suma_tasas / i.numero_personal

    @api.multi
    @api.depends('suma_sueldos', 'minutos_producidos_anio_id')
    def _get_costo_minuto_mod (self):
        for i in self:
            if i.minutos_producidos_anio_id > 0:
                i.costo_minuto_mod = i.suma_sueldos / i.minutos_producidos_anio_id

    @api.multi
    @api.depends('proyeccion_incremento_id', 'costo_minuto_mod')
    @api.onchange('numero_personal')
    def _get_tasa_final(self):
        for i in self:
            valor = (i.proyeccion_incremento_id / 100)* i.costo_minuto_mod
            i.tasa_final = valor + i.costo_minuto_mod

class tra_FormaPago(models.Model):
    _name = 'tra.forma.pago'
    _description = 'Registra las diferentes formas de pago para los clientes'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        #('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]
    name = fields.Char('Nombre', size = 100, required = True)
    recargo = fields.Float('Recargo', size = 9, required = True)
    observacion = fields.Text(u'Observación', required = False)

class tra_Utilidad(models.Model):
    _name = 'tra.utilidad'
    _description = 'Registra valores de utilidades aplicadas de acuerdo a las unidades compradas o a la forma de pago'

    _sql_constraints =[
        ('unique_name', 'unique(name)', 'El nombre de la jornada ya existe'),
        #('unique_codigo', 'unique(codigo)', u'El código de la jornada ya existe'),
    ]

    name = fields.Char('Nombre', size = 100, required = True)
    num_unidades = fields.Float('Num. Unidades', size = 6, required = True)
    porcentaje = fields.Float('Porcentaje Utilidad', size = 3, required = True)
    observacion = fields.Text (u'Observación', required = False)

class tra_Accesorio(models.Model):
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
    observacion = fields.Text ('Observaciones', required = False)
    # Campos Calculados
    valor_total = fields.Float (compute = '_get_valor_total', string = 'Total')

    @api.multi
    @api.depends('costo', 'iva', 'costo')
    @api.onchange('costo', 'iva', 'costo')
    def _get_valor_total (self):
        # Calcula el campo largo total
        for i in self:
            if i.iva and i.costo > 0:
                i.valor_total= ((i.costo * i.iva)/100) + i.costo
            else:
                i.valor_total = 0

class tra_MateriaForro(models.Model):
    _name = 'tra.materia.forro'
    _description = 'Registra el material que el forro de una prenda textil requiere'

    _sql_constraints = [
        ('unique_codigo', 'unique(codigo)', 'Otra prenda tiene el mismo código. Por favor escriba otro código'),
        ('unique_name_tela_talla', 'unique(name, tela_id, talla_id)', 'La prenda ya existe. Escriba otro nombre, tela o talla'),
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
    materias_extras_ids = fields.One2many('tra.materia.forro.extras', 'detail_extra_id', string = 'Materia Prima Extra', store = True)
    accesorios_ids = fields.One2many('tra.materia.forro.accesorio', 'detail_accesorio_id', string = 'Accesorios Extra')

    # Campos Calculados
    largo_total = fields.Float(compute = '_get_largo_total', string = 'Largo Total', store = True)
    ancho_total = fields.Float(compute = '_get_ancho_total', string = 'Ancho Total', store = True)
    piezas_reales = fields.Float(compute = '_get_piezas_reales', string = 'Nro. Piezas', store = True)
    tela_utilizada = fields.Float(compute = '_get_tela_utilizada', string = 'Tela Utilizada (Cuerpo)', store = True)
    costo_tela_cuerpo = fields.Float(compute = '_get_costo_tela_cuerpo', string = 'Costo Tela (Cuerpo)', store = True)
    costo_tela_extra = fields.Float(compute = '_get_costo_tela_extra', string = 'Costo Tela Extra', store = True)
    costo_extras = fields.Float(compute = '_get_costo_extras', string = 'Costo M.P. Extra', store = True)
    costo_accesorios = fields.Float(compute = '_get_costo_accesorios', string = 'Costo Accesorios Extras', store = True)
    total_tela_utilizada = fields.Float(compute = '_get_total_tela_utilizada', string = 'Total Tela Utilizada (Cuerpo + Extra)', store = True)
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Costo Total', store = True)

    @api.multi
    @api.depends('largo_frente', 'largo_manga', 'scrap', 'largo_manga_extra')
    def _get_largo_total (self):
        # Calcula el campo largo total
        for i in self:
            i.largo_total = i.largo_frente + i.largo_manga + i.scrap + i.largo_manga_extra

    @api.multi
    @api.depends('ancho_frente', 'ancho_espalda')
    def _get_ancho_total (self):
        # Calcula el ancho total del Forro
        for i in self:
            i.ancho_total = i.ancho_frente + i.ancho_espalda

    @api.multi
    @api.depends('ancho_tela_id', 'ancho_total')
    def _get_piezas_reales (self):
        # Calcula el numero de piezas reales que salen de la tela escogida
        import math
        for i in self:
            if i.ancho_total > 0:
                piezas = i.ancho_tela_id / i.ancho_total
            else:
                piezas = 0
            t = math.modf(piezas) # math.modf(Decimal) esto devuelve una tupla con la parte decimal y en la posicion 1 la parte entera
            if t[0] >= 0.50: # Si la aparte decimal es mayor a 0,50 entonces baja a 0,50
                piezas= t[1] + 0.50
            else: # Si es menor entonces solamente queda la parte entera
                piezas = t[1]
            i.piezas_reales = piezas

    @api.multi
    @api.depends('piezas_reales', 'largo_total')
    @api.onchange('piezas_reales', 'largo_total')
    def _get_tela_utilizada (self):
        # Calcula la cantidad de tela utilizada para producir la prenda
        import math
        for i in self:
            if i.piezas_reales > 0 :
                tela = math.ceil(1/i.piezas_reales)
                i.tela_utilizada = tela * i.largo_total
            else:
                i.tela_utilizada = 0

    @api.multi
    @api.depends('largo_total', 'costo_tela_id', 'piezas_reales')
    @api.onchange('largo_total', 'costo_tela_id', 'piezas_reales')
    def _get_costo_tela_cuerpo (self):
        # Calcula el costo de tela utilizada en el cuerpo de la prenda
        import math
        for i in self:
            if i.piezas_reales > 0 :
                costo = i.largo_total * i.costo_tela_id
                i.costo_tela_cuerpo = costo / i.piezas_reales
            else:
                i.costo_tela_cuerpo = 0

    @api.multi
    @api.depends('costo_tela_id', 'cantidad_tela_extra')
    @api.onchange('costo_tela_id', 'cantidad_tela_extra')
    def _get_costo_tela_extra (self):
        # Calcula el costo de tela extra utilizada en la prenda
        import math
        for i in self:
            i.costo_tela_extra = i.costo_tela_id * i.cantidad_tela_extra

    @api.multi
    @api.depends('materias_extras_ids')
    @api.onchange('materias_extras_ids')
    def _get_costo_extras(self):
        # Suma el costo de los diferentes materias primas extras
        suma_costos = 0
        for i in self:
            for costo in i.materias_extras_ids:
                suma_costos += costo.total
            i.costo_extras = round(suma_costos, 2)

    @api.multi
    @api.depends('accesorios_ids')
    @api.onchange('accesorios_ids')
    def _get_costo_accesorios(self):
        # Suma el costo de los diferentes accesorios extras
        suma_costos = 0
        for i in self:
            for costo in i.accesorios_ids:
                suma_costos += costo.total
            i.costo_accesorios = round(suma_costos, 2)

    @api.multi
    @api.depends('tela_utilizada', 'cantidad_tela_extra')
    @api.onchange('tela_utilizada', 'cantidad_tela_extra')
    def _get_total_tela_utilizada (self):
        # Suma la cantidad de tela utilizada en el cuepro de laprenda y la cantidad extra
        for i in self:
            i.total_tela_utilizada = i.tela_utilizada + i.cantidad_tela_extra

    @api.multi
    @api.depends('costo_tela_extra', 'costo_tela_cuerpo', 'costo_extras', 'costo_accesorios')
    @api.onchange('costo_tela_extra', 'costo_tela_cuerpo', 'costo_extras', 'costo_accesorios')
    def _get_costo_total(self):
    # Calcula el costo total de la tela utilizada para la prenta textil
        for i in self:
            i.costo_total = i.costo_tela_extra + i.costo_tela_cuerpo + i.costo_extras + i.costo_accesorios

    @api.multi
    @api.depends('talla_id')
    @api.onchange('talla_id')
    def _get_nombre_forro(self):
        nombre = cod = ''
        for i in self:
            if i.name and i.talla_id.name != False:
                i.name = i.name.strip() # Limpia los espacios en blanco del principio y el fin
                nombre = i.name.split(' ') # Devuelve una lista resultado de la división de la cadena por el caracter especificado (Espacio en Blanco)
                for palabra in nombre:
                    cod += palabra[0].upper()
                i.codigo = cod + '0T' + i.talla_id.name
                i.name += ' T' + i.talla_id.name

class tra_MateriaForros_Accesorios(models.Model):
    _name = 'tra.materia.forro.accesorio'
    _description = 'Detalle de Accesorios para Material Forros'

    detail_accesorio_id = fields.Many2one ('tra.materia.forro', 'Materia Prima Forros')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    accesorio_ids = fields.Many2one('tra.accesorio', 'Accesorios', store = True)
    costo = fields.Float(related = 'accesorio_ids.valor_total', string = 'Valor Unitario', digits = (3,2), store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', digits = (3,2), store = True)

    @api.multi
    @api.depends('cantidad', 'accesorio_ids', 'costo')
    @api.onchange('cantidad', 'accesorio_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = round ((i.costo * i.cantidad),2)

class tra_MateriaForro_Extra(models.Model):
    _name = 'tra.materia.forro.extras'
    _description = 'Detalle de Materia Prima Extra para Materia Prima Indirecta'

    detail_extra_id = fields.Many2one ('tra.materia.forro', 'Materia Prima Indirecta')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    materia_extra_ids = fields.Many2one('tra.materia.prima.extra', 'Materia P. Extra', store = True)
    costo = fields.Float(related = 'materia_extra_ids.costo_materia_extra', string = 'Valor Unitario', digits = (3,2), store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', digits = (3,2), store = True)

    @api.multi
    @api.depends('cantidad', 'materia_extra_ids', 'costo')
    @api.onchange('cantidad', 'materia_extra_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = round (i.costo * i.cantidad, 2)


class tra_MateriaPrimaExtra(models.Model):
    _name = 'tra.materia.prima.extra'
    _description = 'Calcula el costo de la materia prima extra utilizada para la elaboración de prendas textiles'

    name = fields.Char('Nombre', size = 100, requiered = True)
    codigo = fields.Char('Código', size = 9, required = True)
    talla_id = fields.Many2one ('tra.talla', 'Talla', required = True)
    tela_id = fields.Many2one('tra.tela', 'Tela', required = True)
    ancho_extra = fields.Float('Ancho Extra', size = 9, required = True)
    factor_ancho = fields.Float('Factor Ancho', size = 9, required = True, default = 1)
    largo_extra = fields.Float('Largo Extra', size = 9, required = True)
    scrap = fields.Float('Scrap', size = 9, required = True)
    observacion = fields.Text('Observaciones', required = False)

    #Campos relacionales
    ancho_tela_id = fields.Float('Ancho Tela', store = False, related = 'tela_id.ancho')
    costo_tela_id = fields.Float('Costo Tela', store = False, related = 'tela_id.costo_total')

    #Campos calculados
    largo_total = fields.Float(compute = '_get_largo_total', string = 'Largo Total', digits=(3,2), store = True)
    ancho_total = fields.Float(compute = '_get_ancho_total', string = 'Ancho Total', digits=(3,2), store = True)
    piezas_reales = fields.Float(compute = '_get_piezas_reales', string = 'Nro. Piezas', digits=(3,2), store = True)
    tela_utilizada = fields.Float(compute = '_get_tela_utilizada', string = 'Tela a utilizar', digits=(3,2),store = True)
    costo_materia_extra = fields.Float(compute = '_get_costo_materia_extra', string = 'Costo Mat. Prima Extra', digits=(3,2), store = True)

    @api.multi
    @api.depends('scrap', 'largo_extra')
    @api.onchange('scrap', 'largo_extra')
    def _get_largo_total(self):
        # Calcula el largo total de la Materia Prima Extra
        for i in self:
            i.largo_total = i.largo_extra + i.scrap

    @api.multi
    @api.depends('ancho_extra', 'factor_ancho')
    @api.onchange('ancho_extra', 'factor_ancho')
    def _get_ancho_total(self):
        for i in self:
            i.ancho_total = i.factor_ancho * i.ancho_extra

    @api.multi
    @api.depends('ancho_tela_id', 'ancho_extra')
    @api.onchange('ancho_tela_id', 'ancho_extra')
    def _get_piezas_reales(self):
        import math
        # Calcula el numero de piezas reales que se obtiene dependiendo del ancho de la telas
        piezas = 0
        for i in self:
            if i.ancho_total > 0:
                piezas = i.ancho_tela_id / i.ancho_total
                t = math.modf(piezas) # math.modf(Decimal) esto devuelve una tupla con la parte decimal y en la posicion 1 la parte entera
                piezas = t[1]
                i.piezas_reales = piezas
            else:
                i.piezas_reales = 0

    @api.multi
    @api.depends('piezas_reales', 'largo_total')
    def _get_tela_utilizada (self):
        import math
        # Calcula la cantidad de tela utilizada
        tela = div = 0
        for i in self:
            if i.piezas_reales > 0 :
                div = 1 / i.piezas_reales
                tela = math.modf(div) # Si el numero tiene decimales entonces se redondea al entero inmediato superior
                if tela[0] > 0:
                    tela = tela[1] + 1
                i.tela_utilizada = tela * i.largo_total

    @api.multi
    @api.depends('largo_extra', 'costo_tela_id', 'piezas_reales')
    def _get_costo_materia_extra (self):
        # Calcula el costo de la materia prima extra en las prendas textiles
        for i in self:
            if i.piezas_reales > 0:
                multip = i.largo_extra * i.costo_tela_id
                i.costo_materia_extra = multip / i.piezas_reales

    @api.multi
    @api.onchange('talla_id')
    def _get_nombre_materia_extra(self):
        for i in self:
            if i.talla_id.name != False and i.name != False:
                i.name += ' T' + i.talla_id.name


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

    #Campos Calculados
    total_gastos_venta = fields.Float(compute = '_get_total_gastos_venta', string = 'Total Gastos Venta', store = True)
    tasa_costo_ventas = fields.Float(compute = '_get_tasa_costo_ventas', string = 'Tasa Costo de Ventas (%)', store = True)

    @api.multi
    @api.depends('gastos_ventas', 'gastos_viajes', 'gastos_operacion', 'gastos_varios', 'servicios_basicos')
    def _get_total_gastos_venta(self):
        for i in self:
            i.total_gastos_venta = i.gastos_ventas + i.gastos_viajes + i.gastos_varios + i.gastos_operacion + i.servicios_basicos

    @api.multi
    @api.depends('total_gastos_venta','venta_anual')
    def _get_tasa_costo_ventas(self):
        for i in self:
            if i.venta_anual > 0:
                i.tasa_costo_ventas = (i.total_gastos_venta / i.venta_anual) * 100


class tra_GastoAdmin(models.Model):
    _name = 'tra.gasto.admin'
    _description = 'Registra y calcula valores de gastos administrativos'

    fecha = fields.Date('Fecha', required = True)
    gastos_admin = fields.Float ('Gastos de Administrativos', size = 11, required = True)
    gastos_operacion = fields.Float ('Gastos Operacionales', size = 11, required = True)
    gastos_varios = fields.Float ('Gastos Varios', size = 11, required = True)
    mantenimiento = fields.Float (u'Mantenimiento', size = 11, required = True)
    egresos_no_operativos = fields.Float(u'Gastos no operativos', size = 11, required = True)
    venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
    observacion = fields.Text ('Observaciones', required = False)

    #Campos calculados
    total_gastos_admin = fields.Float(compute = '_get_total_gastos_admin', string = 'Total Gastos Administrativos', store = True)
    tasa_costo_admin = fields.Float(compute = '_get_tasa_costo_admin', string = 'Total Costos Administrativos (%)', store = True)

    @api.multi
    @api.depends('gastos_admin', 'gastos_operacion', 'mantenimiento', 'gastos_varios', 'egresos_no_operativos', 'venta_anual')
    def _get_total_gastos_admin(self):
        for i in self:
            i.total_gastos_admin = i.gastos_admin + i.gastos_operacion + i.mantenimiento + i.gastos_varios + i.egresos_no_operativos

    @api.one
    @api.depends('total_gastos_admin', 'venta_anual')
    def _get_tasa_costo_admin(self):
        for i in self:
            if self.venta_anual > 0:
                i.tasa_costo_admin = (i.total_gastos_admin / i.venta_anual) * 100


class tra_GastoIndFabricacion(models.Model):
    _name = 'tra.gasto.ind.fabricacion'
    _description = 'Registra y calcula valores de gastos indirectos de fabricacion'

    fecha = fields.Date('Fecha', required = True)
    gastos_produccion = fields.Float (u'Gastos de producción', size = 11, required = True)
    servicios_basicos = fields.Float (u'Servicios básicos', size = 11, required = True)
    mano_obra_indirecta = fields.Float (u'Mano de obra indirecta', size = 11, required = True)
    venta_anual = fields.Float ('Ventas Anuales', size = 11, required = True)
    observacion = fields.Text ('Observaciones', required = False)

    #Campos calculados
    total_gastos_ind_fabricacion = fields.Float(compute = '_get_total_gastos_ind_fabricacion', string = u'Gastos Ind. Fabricación', store = True)
    tasa_costos_gastos_ind_fabricacion = fields.Float(compute = '_get_tasa_costo_ind_fabricacion', string = 'Tasa de Costo Ind. Fab. (%)')

    @api.multi
    @api.depends('gastos_produccion', 'servicios_basicos', 'mano_obra_indirecta')
    def _get_total_gastos_ind_fabricacion(self):
        for i in self:
            i.total_gastos_ind_fabricacion = i.gastos_produccion + i.servicios_basicos + i.mano_obra_indirecta

    @api.multi
    @api.depends()
    def _get_tasa_costo_ind_fabricacion(self):
        for i in self:
            if i.venta_anual > 0:
                i.tasa_costos_gastos_ind_fabricacion = (i.total_gastos_ind_fabricacion / i.venta_anual) * 100

class tra_TiempoProdPrenda(models.Model):
    @api.multi
    @api.onchange('prenda_id')
    @api.depends('prenda_id')
    def _get_tasa_final_id(self):
        for i in self:
            i.tasa_final_id = i.env['tra.mano.obra.directa'].search([], limit = 1).id

    @api.multi
    @api.onchange('tasa_final_id')
    @api.depends('tasa_final_id')
    def _get_gastos_fabricacion_id(self):
        for i in self:
            i.gasto_fabricacion_id = i.env['tra.gasto.ind.fabricacion'].search([], limit = 1).id

    @api.multi
    @api.onchange('tasa_final_id')
    @api.depends('tasa_final_id')
    def _get_gasto_administrativo_id(self):
        for i in self:
            i.gasto_administrativo_id = i.env['tra.gasto.admin'].search([], limit = 1).id

    @api.multi
    @api.onchange('tasa_final_id')
    @api.depends('tasa_final_id')
    def _get_gastos_ventas_id(self):
        for i in self:
            i.gasto_venta_id = i.env['tra.gasto.venta'].search([], limit = 1).id

    _name = 'tra.tiempo.prod.prenda'
    _description = 'Registra el tiempo de producción de una prenda textil'

    tasa_final_id = fields.Many2one('tra.mano.obra.directa', 'Tasa MOD', default = _get_tasa_final_id, store = True)
    minutos = fields.Float('Minutos producción', required = True)
    # Campos relacionales
    tasa_mod = fields.Float('Tasa MOD', store = False, related = 'tasa_final_id.tasa_final')
    gasto_fabricacion_id = fields.Many2one('tra.gasto.ind.fabricacion', u'Gasto de Fabricación', default = _get_gastos_fabricacion_id, store = True)
    gasto_fabricacion = fields.Float(u'Tasa gastos ind. Fab.', store = False, related = 'gasto_fabricacion_id.tasa_costos_gastos_ind_fabricacion')
    gasto_administrativo_id = fields.Many2one('tra.gasto.admin', 'Gastos Administrativos', default = _get_gasto_administrativo_id, store = True)
    gasto_administrativo = fields.Float('Tasa gastos Admin.', store = False, related = 'gasto_administrativo_id.tasa_costo_admin')
    gasto_venta_id = fields.Many2one('tra.gasto.venta','Gastos de Ventas', default = _get_gastos_ventas_id)
    gasto_venta = fields.Float('Tasa gastos Ventas', store = False, related = 'gasto_venta_id.tasa_costo_ventas')
    prenda_id = fields.Many2one('product.template', string = 'Prenda', required = True)
    talla = fields.Char ('Talla', related = 'prenda_id.talla_id.name', store = False)
    tela = fields.Char ('Tela', related = 'prenda_id.tela_id.name', store = False)
    # Campos Calculados
    costo_mod = fields.Float(compute = '_get_costo_mod', string = 'Costo', store = True)
    costo_ind = fields.Float(compute ='_get_costo_ind', string = 'Costo Ind.', store = True)
    costo_gasto_admin = fields.Float(compute = '_get_costo_gasto_admin',string = 'Gasto Admin.', store = True)
    costo_gasto_venta = fields.Float(compute = '_get_costo_gasto_venta', string = 'Gasto Venta', store = True)
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Total Costo', store = True)

    @api.multi
    @api.onchange('minutos')
    @api.depends('tasa_mod')
    def _get_costo_mod(self):
        for i in self:
            i.costo_mod = i.tasa_mod * i.minutos

    @api.multi
    @api.depends('costo_mod')
    def _get_costo_ind(self):
        for i in self:
            i.costo_ind = i.costo_mod * (i.gasto_fabricacion / 100)

    @api.multi
    @api.depends('costo_mod')
    def _get_costo_gasto_admin(self):
        for i in self:
            i.costo_gasto_admin = i.costo_mod * (i.gasto_administrativo / 100)

    @api.multi
    @api.depends('costo_mod')
    def _get_costo_gasto_venta(self):
        for i in self:
            i.costo_gasto_venta = i.costo_mod * (i.gasto_venta / 100)

    @api.multi
    @api.depends('costo_mod')
    def _get_costo_total(self):
        for i in self:
            i.costo_total = i.costo_mod + i.costo_ind + i.costo_gasto_admin + i.costo_gasto_venta


class tra_MaterialesIndirectos(models.Model):
    _name = 'tra.materiales.indirectos'
    _description = 'Registra materiales indirectos para el cálculo de Materia Prima Indirecta'
    _order = 'name'
    # No puede repetirse ni nombre ni código
    _sql_constraints = [
        ('unique_name', 'unique(name)', u'Otro tipo de tela ya tiene este NOMBRE'),
        ('unique_codigo', 'unique(codigo)', u'Otro tipo de tela ya tiene este CÓDIGO'),
    ]

    name = fields.Char('Nombre', size = 100, required = True)
    codigo = fields.Char(u'Código', size = 10, required = True)
    ancho  = fields.Float('Ancho (m.)', size = 6, required = True)
    costo = fields.Float('Costo', size = 6 , required = True)
    iva = fields.Float('IVA (%)', size =3 , required = True)
    costo_total = fields.Float(compute = '_get_costo_total', string = 'Costo Total', digits = (3,2), store = True)
    observacion = fields.Text ('Observación', required = False)

    @api.multi
    @api.depends('costo', 'iva')
    @api.onchange('costo', 'iva')
    def _get_costo_total (self):
        # Calcula costo total por metro de tela
        for i in self:
            i.costo_total = i.costo + ((i.costo * i.iva)/100)

    @api.multi
    @api.onchange('name')
    def _get_uppercase_nombre(self):
        # Cambia a mayúsculas el nombre
        for i in self:
            if i.name != False:
                i.name = i.name.upper()

    @api.multi
    @api.onchange('name')
    def _get_codigo(self):
        # Genera el código de una tela registrada con las primeras letras de cada palabra en el nombre
        nombre = cod = ''
        for i in self:
            if i.name != False:
                i.name = i.name.strip()
                nombre = i.name.split(' ')
                for palabra in nombre:
                    cod += palabra[0].upper()
                i.codigo = cod


class tra_MateriaIndirecta(models.Model):
    #_name = 'tra.materia.indirecta'
    _description = 'Calcula el costo de la materia prima indirecta de una prenda'
    _inherit = 'product.template'
    #prenda_id = fields.Many2one ('product.template', 'Prenda', required = True, store = True)
    #talla = fields.Char('Talla', related = 'prenda_id.talla_id.name', store = False)
    #tela = fields.Char('Tela', related = 'prenda_id.tela_id.name', store = False)
    largo_prenda = fields.Float('Largo de prenda', required = True)
    largo_factor = fields.Float('Factor Largo', required = True)
    ancho_prenda = fields.Float('Ancho de prenda', required = True)
    ancho_factor = fields.Float('Factor Ancho', required = True)
    largo_manga = fields.Float('Largo de manga', required = True)
    manga_factor = fields.Float('Factor Manga', required = True)

    # Campos relacionales
    materiales_indirectos_ids = fields.One2many('tra.materia.indirecta.materiales', 'detail_material_id', string = 'Material Indirecto', store = True)
    materias_extras_ids = fields.One2many('tra.materia.indirecta.extras', 'detail_extra_id', string = 'Materia Prima Extra', store = True)
    accesorios_ids = fields.One2many('tra.materia.indirecta.accesorios', 'detail_accesorio_id', string = 'Accesorios', store = True)

    # Campos calculados
    vivo_largo = fields.Float(compute = '_get_vivo_largo', string = 'Vivo en Largo', store = True)
    vivo_ancho = fields.Float(compute = '_get_vivo_ancho', string = 'Vivo en Ancho', store = True)
    vivo_manga = fields.Float(compute = '_get_vivo_manga', string = 'Vivo en Manga', store = True)
    costo_vivo = fields.Float(compute = '_get_costo_vivo', string = 'Costo de Vivo', store = True)
    suma_materiales = fields.Float(compute = '_get_suma_materiales', string = 'Total M.P. Indirecta', store = True)
    suma_extras = fields.Float(compute = '_get_suma_extras', string = 'Total M.P. Extra', store = True)
    suma_accesorios = fields.Float(compute = '_get_suma_accesorios', string = 'Total Accesorios', store = True)
    costo_materia_indirecta = fields.Float(compute= '_get_costo_materia_indirecta', string = 'Costo Total MPI', store = True)

    @api.multi
    @api.depends('largo_prenda','largo_factor')
    @api.onchange('largo_prenda','largo_factor')
    def _get_vivo_largo(self):
        for i in self:
            i.vivo_largo = i.largo_prenda * i.largo_factor

    @api.multi
    @api.depends('ancho_prenda','ancho_factor')
    @api.onchange('ancho_prenda','ancho_factor')
    def _get_vivo_ancho(self):
        for i in self:
            i.vivo_ancho = i.ancho_prenda * i.ancho_factor

    @api.multi
    @api.depends('largo_manga','manga_factor')
    @api.onchange('largo_manga','manga_factor')
    def _get_vivo_manga(self):
        for i in self:
            i.vivo_manga = i.largo_manga * i.manga_factor

    @api.multi
    @api.depends('vivo_largo', 'vivo_ancho', 'vivo_manga')
    @api.onchange('vivo_largo', 'vivo_ancho', 'vivo_manga')
    def _get_costo_vivo(self):
        for i in self:
            costo_tela = i.env['tra.tela'].search([('name', '=', i.tela_id.name)]).costo_total
            i.costo_vivo = (i.vivo_largo + i.vivo_ancho + i.vivo_manga) * costo_tela

    @api.multi
    @api.depends('materiales_indirectos_ids')
    @api.onchange('materiales_indirectos_ids')
    def _get_suma_materiales(self):
        for i in self:
            suma = 0
            for j in i.materiales_indirectos_ids:
                suma += j.total
            i.suma_materiales = round(suma, 2)

    @api.multi
    @api.depends('materias_extras_ids')
    @api.onchange('materias_extras_ids')
    def _get_suma_extras(self):
        for i in self:
            suma = 0
            for j in i.materias_extras_ids:
                suma += j.total
            i.suma_extras = round(suma, 2)

    @api.multi
    @api.depends('accesorios_ids')
    @api.onchange('accesorios_ids')
    def _get_suma_accesorios(self):
        for i in self:
            suma = 0
            for j in i.accesorios_ids:
                suma += j.total
            i.suma_accesorios = round (suma, 2)

    @api.multi
    @api.depends('suma_materiales', 'suma_extras', 'suma_accesorios', 'costo_vivo')
    @api.onchange('suma_extras','suma_accesorios', 'costo_vivo')
    def _get_costo_materia_indirecta(self):
        for i in self:
            i.costo_materia_indirecta = i.costo_vivo + i.suma_materiales + i.suma_extras + i.suma_accesorios


class tra_MateriaIndirecta_Materiales(models.Model):
    _name = 'tra.materia.indirecta.materiales'
    _description = 'Detalle de Materiales Indirectos para el calculo del costo de Materia prima indirecta'

    detail_material_id = fields.Many2one ('tra.materia.indirecta', 'Materia Prima Indirecta')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    material_ids = fields.Many2one('tra.materiales.indirectos', 'Materiales Indirectos', store = True)
    costo = fields.Float(related = 'material_ids.costo_total', string = 'Valor Unitario', digits = (3,2), store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', digits = (3,2), store = True)

    @api.multi
    @api.depends('cantidad', 'material_ids', 'costo')
    @api.onchange('cantidad', 'material_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = i.costo * i.cantidad


class tra_MateriaIndirecta_Accesorios(models.Model):
    _name = 'tra.materia.indirecta.accesorios'
    _description = 'Detalle de Accesorios para Materia prima indirecta'

    detail_accesorio_id = fields.Many2one ('tra.materia.indirecta', 'Materia Prima Indirecta')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    accesorio_ids = fields.Many2one('tra.accesorio', 'Accesorios', store = True)
    costo = fields.Float(related = 'accesorio_ids.valor_total', string = 'Valor Unitario', digits = (3,2), store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', digits = (3,2), store = True)

    @api.multi
    @api.depends('cantidad', 'accesorio_ids', 'costo')
    @api.onchange('cantidad', 'accesorio_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = i.costo * i.cantidad

class tra_MateriaIndirecta_Extra(models.Model):
    _name = 'tra.materia.indirecta.extras'
    _description = 'Detalle de Materia Prima Extra para Materia Prima Indirecta'

    detail_extra_id = fields.Many2one ('tra.materia.indirecta', 'Materia Prima Indirecta')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    materia_extra_ids = fields.Many2one('tra.materia.prima.extra', 'Materia P. Extra', store = True)
    costo = fields.Float(related = 'materia_extra_ids.costo_materia_extra', string = 'Valor Unitario', digits = (3,2), store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', digits = (3,2), store = True)

    @api.multi
    @api.depends('cantidad', 'materia_extra_ids', 'costo')
    @api.onchange('cantidad', 'materia_extra_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = i.costo * i.cantidad

class tra_MateriaDirecta(models.Model):
    #_name = 'tra.materia.directa'
    _description = 'Registra y calcula costos de materia prima de una prenda textil'
    _inherit = 'product.template'

    #prenda_id = fields.Many2one('product.template', 'Prenda', required = True, store = True)
    #talla = fields.Char('Talla', related = 'prenda_id.talla_id.name', store = False)
    #tela = fields.Char('Tela', related = 'prenda_id.tela_id.name', store = False)
    ancho_tela = fields.Float('Ancho de Tela (m.)', related = 'tela_id.ancho', store = False)
    costo_tela = fields.Float('Costo de Tela x m.', related = 'tela_id.costo')
    largo_frente = fields.Float('Largo de Frente', size = 6, required = True)
    ancho_frente = fields.Float('Ancho de Frente', size = 6, required = True)
    largo_espalda = fields.Float('Largo de Espalda', size = 6, required = True)
    ancho_espalda = fields.Float('Ancho de Espalda', size = 6, required = True)
    largo_manga = fields.Float('Largo de Manga', size = 6, required = True)
    ancho_manga = fields.Float('Ancho de Manga', size = 6, required = True)
    scrap = fields.Float('Scrap', size = 6, required = True)
    largo_person = fields.Float('Tamaño Personalizado', size = 6, required = False)
    tela_extra = fields.Float('Tela Extra', size = 6, required = False)
    detalles_ids = fields.One2many('tra.materia.directa.detail', 'detail_id', string = 'Accesorios')
    # Campos Calculados
    total_largo = fields.Float(compute = '_get_total_largo', string = 'Total Largo', store = True)
    total_ancho = fields.Float(compute = '_get_total_ancho', string = 'Total Ancho', store = True)
    num_piezas = fields.Float(compute = '_get_num_piezas', string = u'Número de Piezas', store = True)
    cantidad_tela = fields.Float(compute = '_get_cantidad_tela', string = 'Cantidad Tela', store = True)
    total_tela_utilizada = fields.Float(compute = '_get_total_tela_utilizada', string = 'Total Tela Util.', store = True)
    costo_tela_cuerpo = fields.Float(compute = '_get_costo_tela_cuerpo', string = 'Costo Tela Cuerpo', store = True)
    costo_tela_extra = fields.Float(compute = '_get_costo_tela_extra', string = 'Costo Tela Extra', store = True)
    costo_materia_extra = fields.Float(compute = '_get_costo_materia_extra', string = 'Costo Mat. Prima Extra', store = True)
    total_costo_tela = fields.Float(compute = '_get_total_costo_tela', string = 'Suma Costos Tela', store = True)

    @api.multi
    @api.depends('largo_frente','largo_manga','scrap','largo_person')
    @api.onchange('largo_frente','largo_manga','scrap','largo_person')
    def _get_total_largo(self):
        for i in self:
            i.total_largo = i.largo_frente + i.largo_manga + i.scrap + i.largo_person

    @api.multi
    @api.depends('ancho_frente','ancho_espalda')
    @api.onchange('ancho_frente','ancho_espalda')
    def _get_total_ancho(self):
        for i in self:
            i.total_ancho = i.ancho_frente + i.ancho_espalda

    @api.multi
    @api.depends('total_ancho', 'ancho_tela')
    @api.onchange('total_ancho', 'ancho_tela')
    def _get_num_piezas(self):
        import math
        for i in self:
            if i.total_ancho > 0:
                piezas = i.ancho_tela / i.total_ancho
            else:
                piezas = 0
            t = math.modf(piezas) # math.modf(Decimal) esto devuelve una tupla con la parte decimal y en la posicion 1 la parte entera
            if t[0] >= 0.50: # Si la aparte decimal es mayor a 0,50 entonces baja a 0,50
                piezas= t[1] + 0.50
            else: # Si es menor entonces solamente queda la parte entera
                piezas = t[1]
            i.num_piezas = piezas

    @api.multi
    @api.depends('num_piezas', 'total_largo')
    @api.onchange('num_piezas', 'total_largo')
    def _get_cantidad_tela (self):
        import math
        for i in self:
            if i.num_piezas > 0:
                multip = 1 / i.num_piezas
            else:
                multip = 0
            t = math.modf(multip) # math.modf(Decimal) esto devuelve una tupla con la parte decimal y en la posicion 1 la parte entera
            if t[0] > 0: # Si la aparte decimal es mayor a 0,50 entonces baja a 0,50
                multip = t[1] + 1
            else: # Si es menor entonces solamente queda la parte entera
                multip = t[1]
            i.cantidad_tela = multip * i.total_largo

    @api.multi
    @api.depends('costo_tela', 'total_largo', 'num_piezas')
    @api.onchange('costo_tela', 'total_largo', 'num_piezas')
    def _get_costo_tela_cuerpo(self):
        for i in self:
            if i.num_piezas > 0:
                i.costo_tela_cuerpo = (i.total_largo * i.costo_tela) / i.num_piezas

    @api.multi
    @api.depends('tela_extra', 'costo_tela')
    @api.onchange('tela_extra', 'costo_tela')
    def _get_costo_tela_extra(self):
        for i in self:
            i.costo_tela_extra = i.costo_tela * i.tela_extra

    @api.multi
    @api.depends('cantidad_tela', 'tela_extra')
    @api.onchange('cantidad_tela', 'tela_extra')
    def _get_total_tela_utilizada(self):
        for i in self:
            i.total_tela_utilizada = i.cantidad_tela + i.tela_extra

    @api.multi
    @api.depends('detalles_ids')
    def _get_costo_materia_extra(self):
        for i in self:
            suma = 0
            for j in i.detalles_ids:
                suma += j.total
            i.costo_materia_extra = suma

    @api.multi
    @api.depends('costo_tela_extra', 'costo_tela_cuerpo', 'costo_materia_extra')
    @api.onchange('costo_tela_extra', 'costo_tela_cuerpo', 'costo_materia_extra')
    def _get_total_costo_tela(self):
        for i in self:
            i.total_costo_tela = i.costo_tela_cuerpo + i.costo_tela_extra + i.costo_materia_extra


class tra_MateriaDirecta_Detail(models.Model):
    _name = 'tra.materia.directa.detail'
    _description = 'Registra los accesorios de materia prima directa'

    detail_id = fields.Many2one ('tra.materia.directa', 'Materia Prima Prenda')
    cantidad = fields.Integer('Cant.', default = 1, required = True)
    materia_extra_ids = fields.Many2one('tra.materia.prima.extra', 'Materia P. Extra', store = True)
    costo = fields.Float(related = 'materia_extra_ids.costo_materia_extra', string = 'Valor Unitario', store = True)
    total = fields.Float(compute = '_get_valor_total', string = 'Total', store = True)

    @api.multi
    @api.depends('cantidad', 'materia_extra_ids', 'costo')
    @api.onchange('cantidad', 'materia_extra_ids', 'costo')
    def _get_valor_total(self):
        for i in self:
            i.total = i.costo * i.cantidad
