from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestStockBarcodeTransferWizard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Incoming picking type
        cls.wizard_incoming = cls.env["stock.barcode.transfer.wizard"].create({
            "wizard_mode": cls.env.ref("stock.picking_type_in").id,
        })

        # Outgoing picking type
        cls.wizard_outgoing = cls.env["stock.barcode.transfer.wizard"].create({
            "wizard_mode": cls.env.ref("stock.picking_type_out").id,
        })

        # Internal trasfer picking type
        cls.wizard_internal = cls.env["stock.barcode.transfer.wizard"].create({
            "wizard_mode": cls.env.ref("stock.picking_type_internal").id,
        })

        cls.product1 = cls.env["product.template"].create({
            "name": "Test Product 1",
            "barcode": "123456789",
        })


    def test_01_check_product_barcode_parsing(self):
        """
        Try to create a product with a GS1 barcode and check that the
        relevant fields are correctly parsed and filled in.
        """
        # Barcode structure:
        # (01)123456789 - GTIN ("barcode")
        # (17)300102 - Expiration date (YYMMDD)
        # (10)222222 - Lot number
        # (11)301225 - Production date (YYMMDD)
        # (240)TESTCODE - Product code
        barcode = "(01)123456789(17)300102(10)222222(11)301225(240)TESTCODE"
        product = self.env["product.template"].create({
            "name": "Test Product",
        })
        product.parse_gs1_barcode(barcode)

        self.assertEqual(product.barcode, "123456789")
        self.assertEqual(product.default_code, "TESTCODE")

    def test_02_test_product_information(self):
        """
        Test that product information is correctly set up
        """
        wiz  = self.wizard_incoming
        wiz.barcode = "(01)123456789"
        with self.assertRaises(UserError):
            # Product is not tracked by lot, should raise error        
            wiz._onchange_barcode()
        # TODO: set product to be tracked by lot, test again
        print(wiz.current_product_id)

    def test_03_test_scanning_incoming_product(self):
        """
        Test scanning incoming product in two parts
        """
        wiz  = self.wizard_incoming
        wiz.barcode = "(01)123456789"
        # TODO: scanning the product should not raise an error
        # wiz._onchange_barcode()
