# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, exceptions, _
import datetime
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class repaircustomization(models.Model):
    _name = 'repair.modules'
    _rec_name = 'rep_service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    part_no = fields.Integer(string="Part no")
    my_sequence = fields.Char( String="Sequence")
    rep_service = fields.Char(String="Repair Service")
    customer_name = fields.Char(string="Customer Name")
    mileage = fields.Float(string=" Total Mileage", compute='get_mileage')
    date_reg = fields.Date(string="Date of registeration")
    pickup = fields.Boolean(string="self pickup", default=False)
    service = fields.Many2one('service.type', string="Service Type", required=True)
    previous_services = fields.Many2one('prev.services', string="Previous Services", required=True)
    contact_details = fields.One2many('contact.details', 'contact_number', string="Contact Details")
    # car_documents = fields.Binary(string="Car documentation sheet")
    pickup_time = fields.Selection([('one_week', 'one week'), ('one_month', 'one month')], string="Pickup Time",
                                   compute='get_pickup_time')

    @api.model
    def create(self, vals_list):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        name = self.env['ir.sequence'].next_by_code('repair.auto.generate.sequence')
        _logger.warning(
            "list: %s" % vals_list)
        vals_list['my_sequence']=name
        templates = super(repaircustomization, self).create(vals_list)
        # print(templates)
        # if templates.car:
        #     templates.barcode = templates.car.model_no
        return templates

    # @api.depends('warehouse_id')
    def get_contact_results(self):
        loc_domain = [('country_code', '=', '92'), ('contact_number', '=', self.id)]
        data = self.env['contact.details'].search(loc_domain)
        self.contact_details = data

    @api.depends('pickup')
    def get_mileage(self):
        for rec in self:
            _logger.warning(
                "computed: %s" % rec.pickup)

            if rec.pickup:
                rec.mileage = 50
            else:
                rec.mileage = 20

    @api.onchange('service')
    def onchng_services(self):
        self.part_no = 55
        getrec = self.env['service.type'].search([('insurance', '=', 'insured')])
        _logger.warning(
            "got records: %s" % getrec)

    @api.depends('service')
    def get_pickup_time(self):
        _logger.warning(
            "computed: %s" % self.service)

        if self.service:
            self.pickup_time = 'one_week'
        else:
            self.pickup_time = 'one_month'

    @api.onchange('customer_name')
    def onchng_customer_name(self):
        if self.date_reg == False:
            self.date_reg = datetime.date.today()

        getrec = self.env['repair.modules'].search([('customer_name', '=', 'xyz')])
        _logger.warning(
            "got records: %s" % getrec)


class temp_inheritcls(models.Model):
    _inherit = 'product.template'

    car = fields.Many2one('car.modules', string="car")

class temp_inheritrep(models.Model):
    _inherit = 'account.move'

    repair = fields.Many2one('repair.modules', string="Repair")




class address_inherit(models.Model):
    _inherit = 'account.move'

    address = fields.Many2one('contact.details', string="Address Details")


class service(models.Model):
    _name = 'service.type'
    _rec_name = 'type_name'

    type_name = fields.Char(string="Service Type Name")
    insurance = fields.Selection([('insured', 'insured'), ('not_insured', 'not_insured')], string="Insurance")


class previousservices(models.Model):
    _name = 'prev.services'
    _rec_name = 'first_service'

    first_service = fields.Char(string="First service type")
    first_service_date = fields.Date(string="First Service Date")
    other_services = fields.Boolean(string="Other services", default=False)
    last_service = fields.Char(string="Last service Type")
    last_service_date = fields.Date(string="Last Service Date")


class contact(models.Model):
    _name = 'contact.details'
    _rec_name = 'contact_id'

    contact_number = fields.Many2one('repair.modules', string='Contact Number')
    address = fields.Char(string="Address")
    contact_id = fields.Char(string="Contact ID")
    country_code = fields.Selection([('92', '92'), ('04', '04')], string="Country Code")
    State = fields.Selection([('Pakistan', 'Pakistan'), ('Arizona_US', 'Arizona,US')], string="State")
