from odoo import api, models, fields, exceptions, _
import datetime
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class carwizard(models.TransientModel):
    _name = 'carrepair.modules'

    rep_orders_id = fields.Integer(String="ID")
    repair_details = fields.Many2one('repair.modules', string="Select Repair Details", required=True)
    date_of_repair = fields.Date(string="Date of Repair")
    car_select = fields.Many2one('car.modules', string="Select Car Details", required=True)

    def createtorder(self):

        rec = self.env['reporders.modules'].create({
            'repair_select': self.repair_details.id,
            'car_details_select': self.car_select.id ,
            'date_of_rep': self.date_of_repair,
            # 'rep_orders_id' : self.id,

        })

