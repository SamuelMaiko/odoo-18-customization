from odoo import models, fields

class VendorReference(models.Model):
    _name = 'vendor.reference'
    _description = 'Vendor Reference for RFQ'

    vendor_id = fields.Many2one('res.partner', string="Vendor", required=True)
    reference = fields.Char(string="Vendor Reference", required=True)
    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order", required=True)
