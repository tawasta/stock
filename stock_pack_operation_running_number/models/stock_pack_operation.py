from odoo import models, fields, api


class StockPackOperation(models.Model):

    _inherit = 'stock.pack.operation'

    @api.multi
    def _compute_running_number(self):
        '''Assigns a running number to the pack operation line,
        starting from 1 onwards '''
        for line in self:
            pack_lines = self.search(args=[('picking_id',
                                            '=',
                                            line.picking_id.id)])
            i = 1
            for pack_line in pack_lines:
                if pack_line.id == line.id:
                    line.running_number = i
                    break
                i += 1

    running_number = fields.Integer(
        compute=_compute_running_number,
        string='Running Number'
    )
