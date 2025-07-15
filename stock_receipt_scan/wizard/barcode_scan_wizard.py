from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
import re

import logging
_logger = logging.getLogger(__name__)



def parse_gs1_barcode(barcode_str):
    """
    Palauttaa sanakirjan AI-koodeista, esim: {'01': 'GTIN', '10': 'LOT', '17': 'YYMMDD'}
    """
    pattern = r"\((\d{2})\)([^\(]+)"
    matches = re.findall(pattern, barcode_str)
    return {ai: value.strip() for ai, value in matches}


class BarcodeScanWizard(models.TransientModel):
    _name = 'barcode.scan.wizard'
    _description = 'Barcode Scan Wizard'

    picking_id = fields.Many2one('stock.picking', required=True)
    barcode = fields.Char(string="Scan Barcode")

    scanned_line_ids = fields.One2many('barcode.scan.line', 'wizard_id', string="Scanned Lines")

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if not self.barcode:
            return

        gs1_data = parse_gs1_barcode(self.barcode)
        product_code = gs1_data.get("01")
        lot_name = gs1_data.get("10")
        expiration_raw = gs1_data.get("17")

        if not product_code:
            raise UserError("The barcode does not contain the (01) product identifier.")

        expiration_date = None
        if expiration_raw and re.match(r"^\d{6}$", expiration_raw):
            try:
                expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
            except ValueError:
                raise UserError("The expiration date in the barcode is invalid.")

        product = self.env['product.product'].search([
            '|',
            ('barcode', '=', product_code),
            ('default_code', '=', product_code),
        ], limit=1)

        if not product:
            raise UserError(f"No product found with barcode {product_code}.")

        moves = self.picking_id.move_ids_without_package.filtered(lambda m: m.product_id == product)
        if not moves:
            raise UserError(f"The product '{product.display_name}' is not in the current transfer.")

        lot = self.env['stock.lot'].search([
            ('product_id', '=', product.id),
            ('name', '=', lot_name)
        ], limit=1)

        if not lot:
            raise UserError(f"Product found in transfer, but no lot with name '{lot_name}' was found.")

        already_scanned = self.scanned_line_ids.filtered(
            lambda l: l.product_id == product and l.lot_id == lot
        )
        if already_scanned:
            raise UserError(f"Lot '{lot.name}' for product '{product.display_name}' has already been scanned.")

        self.write({
            'scanned_line_ids': [(0, 0, {
                'product_id': product.id,
                'lot_id': lot.id,
                'lot_name': lot.name,
                'expiration_date': expiration_date,
            })]
        })



        self.barcode = ''  # tyhjennetään kenttä automaattisesti seuraavaa skannausta varten

    def action_save_lines(self):
        self.ensure_one()
        _logger.info("scanned lines: %s", self.scanned_line_ids)

        for line in self.scanned_line_ids:
            _logger.info("==PRODUCT %s", line.product_id)
            # Etsi siirto (stock.move), joka vastaa tuotetta
            move = self.picking_id.move_ids_without_package.filtered(
                lambda m: m.product_id == line.product_id
            )
            if not move:
                raise UserError(f"No stock move found for product '{line.product_id.display_name}'.")

            self.env['stock.move.line'].create({
                'picking_id': self.picking_id.id,
                'move_id': move.id,
                'company_id': self.picking_id.company_id.id,
                'product_id': line.product_id.id,
                'product_uom_id': move.product_uom.id,
                'quantity': 1.0,  # Muuta tarvittaessa, esim. jos haluat GS1:stä määrän
                'lot_id': line.lot_id.id,
                'lot_name': line.lot_name,
                'expiration_date': line.expiration_date,
                'location_id': self.picking_id.location_id.id,
                'location_dest_id': self.picking_id.location_dest_id.id,
                'date': fields.Datetime.now(),
            })



class BarcodeScanLine(models.TransientModel):
    _name = 'barcode.scan.line'
    _description = 'Scanned Barcode Line'

    wizard_id = fields.Many2one('barcode.scan.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product",)
    lot_id = fields.Many2one('stock.lot', string="Lot", readonly=True)
    lot_name = fields.Char(string="Lot/SN", readonly=True)
    expiration_date = fields.Date(string="Expiration", readonly=True)


