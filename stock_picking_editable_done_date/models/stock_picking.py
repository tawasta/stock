# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    date_done = fields.Datetime(readonly=False)
