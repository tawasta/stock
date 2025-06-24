from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class StockReceipt(models.Model):
    _name = "stock.receipt"
    _description = "Stock Receipt"

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        readonly=True,
    )
    create_date = fields.Datetime(
        string='Date',
        readonly=True,
    )
    barcode_input = fields.Char(
        string="Scan Barcode",
        help="Scan product barcode to add a line",
    )
    line_ids = fields.One2many(
        'stock.receipt.line',
        'receipt_id',
        string='Lines',
    )

    move_selection_ids = fields.Many2many(
        'stock.move',
        string='Select Stock Moves',
        help='Valitse yksi varastosiirroista jatkaaksesi',
    )

    @api.onchange('barcode_input')
    def _onchange_barcode_input(self):
        if not self.barcode_input:
            return
        product = self.env['product.product'].search(
            ['|', ('barcode', '=', self.barcode_input), ('default_code', '=', self.barcode_input)],
            limit=1,
        )
        if not product:
            return
        moves = self.env['stock.move'].search([('product_id', '=', product.id)])
        if not moves:
            return

        if len(moves) > 1:
            # Aseta move_selection_ids mahdolliset movesiksi
            self.move_selection_ids = moves
            # Tyhjennä barcode_input odottamaan käyttäjän valintaa ja jatkoa
            self.barcode_input = False
        else:
            move = moves[0]
            existing_line = self.line_ids.filtered(lambda l: l.stock_move_id == move)
            if existing_line:
                existing_line.quantity += 1.0
            else:
                self.line_ids |= self.line_ids.new({
                    'product_id': product.id,
                    'barcode': self.barcode_input,
                    'quantity': 1.0,
                    'stock_move_id': move.id,
                })
            self.barcode_input = False

    @api.onchange('move_selection_ids')
    def _onchange_move_selection_ids(self):
        # Jos valittu vain yksi move
        if len(self.move_selection_ids) == 1:
            move = self.move_selection_ids[0]
            existing_line = self.line_ids.filtered(lambda l: l.stock_move_id == move)
            if existing_line:
                existing_line.quantity += 1.0
            else:
                self.line_ids |= self.line_ids.new({
                    'product_id': move.product_id.id,
                    'barcode': False,
                    'quantity': 1.0,
                    'stock_move_id': move.id,
                })
            self.move_selection_ids = False




class StockReceiptLine(models.Model):
    _name = "stock.receipt.line"
    _description = "Stock Receipt Line"

    receipt_id = fields.Many2one(
        'stock.receipt',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )
    barcode = fields.Char(
        string='Barcode',
    )
    quantity = fields.Float(
        string='Quantity',
        default=1.0,
    )
    stock_move_id = fields.Many2one(
        'stock.move',
        string='Stock Move',
        readonly=True,
    )
    stock_picking_id = fields.Many2one(
        related='stock_move_id.picking_id',
        string='Picking',
        readonly=True,
    )
