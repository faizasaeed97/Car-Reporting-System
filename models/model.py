# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class carcustomization(models.Model):
    _name = 'car.modules'
    _rec_name = 'model_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    model_no = fields.Char(string='Model no')
    my_sequence_one = fields.Char(string='Sequence Number')
    color = fields.Char(string='Color')
    mileage = fields.Float(string='Mileage', compute='get_mileage')
    width = fields.Float(string='Width')
    height = fields.Float(string='Height')
    wheel_base = fields.Float(string='Wheel base')
    turning_radius = fields.Float(string='Turning Radius')
    no_of_cylinders = fields.Integer(string='No of Cylinders')
    manufacturing_date = fields.Date(string='Manufacturing date')
    for_sale = fields.Boolean(string='For sale', default=False)
    car_color = fields.Many2one('car.color', string='Car Color', required=True)
    engine_specs = fields.Many2one('engine.specs', string='Engine Specifications', required=True)
    airbags = fields.One2many('airbags.details', 'airbag_id', string="airbag")
    # engine_specs_sheet = fields.Binary (string = 'Engine specification sheet')
    buy = fields.Selection([('i', 'installment'), ('o', 'one_time_payment')], string='Payment method')


    def car_cron(self):
        getrec3 = self.env['car.modules'].search([])
        for rec in getrec3:

            _logger.warning(
                "Abcd")
            if rec.buy:
                rec.for_sale = False
            else:
                rec.for_sale = True



    @api.model
    def create(self, vals_list):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        name = self.env['ir.sequence'].next_by_code('car.auto.generate.sequence')
        # _logger.warning(
        #     "list: %s" % vals_list)
        vals_list['my_sequence_one'] = name
        templates = super(carcustomization, self).create(vals_list)
        # print(templates)
        # if templates.car:
        #     templates.barcode = templates.car.model_no
        return templates

    # def get_airbags_results(self):
    #     loc_domain = [('no_of_airbags', '=', '2'), ('airbag_id', '=', self.id)]
    #     data = self.env['contact.details'].search(loc_domain)
    #     self.contact_details = data

    @api.depends('model_no')
    def get_mileage(self):
        for rec in self:
            # _logger.warning(
            #     "computed: %s" % rec.model_no)

            if rec.model_no:
                rec.mileage = 50
            else:
                rec.mileage = 20

    @api.onchange('manufacturing_date')
    def onchng_services(self):
        self.for_sale = True
        getrec2 = self.env['service.type'].search([('insurance', '=', 'insured')])
        # _logger.warning(
        #     "got records: %s" % getrec2)

    def test_name(self):
        view = self.env.ref('car_customization.create_car_wizard')
        return {
            'view_mode': 'form',
            'res_model': 'carrepair.modules',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': view.id,
            'context': self.env.context,
        }


class color(models.Model):
    _name = 'car.color'
    _rec_name = 'body_color'

    body_color = fields.Char(string='Body Color')
    interior_color = fields.Char(string='Interior Color')


class enginespecs(models.Model):
    _name = 'engine.specs'
    _rec_name = 'model'

    model = fields.Char(string='Engine Model')
    engine_displacement = fields.Float(string='Engine Displacement')
    horsepower = fields.Integer(string='Horsepower')
    power_train = fields.Selection([('a', 'FWD'), ('b', 'RWD'), ('c', '4WD')], string=' Power Train')


class airbags(models.Model):
    _name = 'airbags.details'
    _rec_name = 'airbag_type'

    airbag_id = fields.Many2one('car.modules', string='Airbag Type ID')
    airbag_type = fields.Selection([('d', 'Side Airbags'), ('e', 'Front Airbags'), ('f', 'Knee Airbags')],
                                   string=' Airbags Type')
    no_of_airbags = fields.Integer(string='No of Airbags')


class temp_inheritcar(models.Model):
    _inherit = 'sale.order'

    car_one = fields.Many2one('car.modules', string="Car")
