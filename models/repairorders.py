from odoo import api, models, fields, exceptions, _
import datetime
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class repairorders(models.Model):
    _name = 'reporders.modules'
    _rec_name = 'repair_select'

    repair_select = fields.Many2one('repair.modules', string="Select Repair Details")
    my_sequence_three= fields.Char (String="Sequence No.")
    date_of_rep = fields.Date(string="Date of Repair")
    car_details_select = fields.Many2one('car.modules', string="Select Car Details")
    customer_name = fields.Char(related='repair_select.customer_name')

    @api.model
    def create(self, vals_list):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        name = self.env['ir.sequence'].next_by_code('repair.auto.generate.sequence')
        _logger.warning(
            "list: %s name %s",  str(vals_list),str(name))
        vals_list['my_sequence_three'] = name
        templates = super(repairorders, self).create(vals_list)
        # print(templates)
        # if templates.car:
        #     templates.barcode = templates.car.model_no
        return templates

