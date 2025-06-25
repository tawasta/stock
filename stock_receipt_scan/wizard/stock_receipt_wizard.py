from odoo import models, fields, api

class StockReceiptWizard(models.TransientModel):
    _name = "stock.receipt.wizard"
    _description = "Stock Receipt Wizard"

    barcode_input = fields.Char(string="Scan Barcode")
    line_ids = fields.One2many('stock.receipt.wizard.line', 'wizard_id', string='Lines')

    @api.onchange('barcode_input')
    def _onchange_barcode_input(self):
        if not self.barcode_input:
            return

        product = self.env['product.product'].search([
            '|', ('barcode', '=', self.barcode_input), ('default_code', '=', self.barcode_input)
        ], limit=1)
        if not product:
            return {
                'warning': {
                    'title': "Product not found",
                    'message': f"No product found with barcode '{self.barcode_input}'.",
                }
            }

        move = self.env['stock.move'].search([('product_id', '=', product.id), ('state', '=', 'assigned')], order='date asc', limit=1)
        if not move:
            return {
                'warning': {
                    'title': "Stock move not found",
                    'message': f"No stock move found for product '{product.name}'.",
                }
            }

        existing_line = self.line_ids.filtered(lambda l: l.stock_move_id.id == move.id)
        if existing_line:
            existing_line.quantity += 1.0
        else:
            self.line_ids |= self.env['stock.receipt.wizard.line'].new({
                'product_id': product.id,
                'barcode': self.barcode_input,
                'quantity': 1.0,
                'stock_move_id': move.id,
            })
        self.barcode_input = False

    def validate_receipt_lines(self):
        # TODO: Lisää validointisäännöt tänne tarvittaessa
        pass

    def post_process_receipt_line(self, receipt_line):
        # TODO: Lisää myöhemmin riveihin liittyvä lisälogiikka tänne
        pass

    def action_confirm(self):
        # Suorita validointi ennen vastaanoton luontia
        self.validate_receipt_lines()
        receipt = self.env['stock.receipt'].create({'user_id': self.env.user.id})
        for line in self.line_ids:
            receipt_line = self.env['stock.receipt.line'].create({
                'receipt_id': receipt.id,
                'product_id': line.product_id.id,
                'barcode': line.barcode,
                'quantity': line.quantity,
                'stock_move_id': line.stock_move_id.id,
            })
            # Kutsu tyhjää apufunktiota rivin luonnin jälkeen
            self.post_process_receipt_line(receipt_line)

        # Kirjaa chatteriin viesti vastaanotosta
        lines_info = "\n".join([
            f"- {line.product_id.display_name} (Barcode: {line.barcode or 'N/A'}), Quantity: {line.quantity}"
            for line in self.line_ids
        ])

        body = (
            f"Stock receipt confirmed by {self.env.user.name}.\n\n"
            f"Received lines:\n{lines_info}"
        )
        receipt.message_post(body=body, subtype_xmlid='mail.mt_comment')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.receipt',
            'res_id': receipt.id,
            'view_mode': 'form',
        }

class StockReceiptWizardLine(models.TransientModel):
    _name = "stock.receipt.wizard.line"
    _description = "Stock Receipt Wizard Line"

    wizard_id = fields.Many2one('stock.receipt.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', required=True)
    barcode = fields.Char()
    quantity = fields.Float(default=1.0)
    stock_move_id = fields.Many2one('stock.move')
