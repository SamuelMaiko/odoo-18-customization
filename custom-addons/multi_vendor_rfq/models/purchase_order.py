from odoo import models, fields, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_id = fields.Many2one('res.partner', string='Vendor', required=False, change_default=True, tracking=True, check_company=True, help="You can find a vendor by its Name, TIN, Email, or Internal Reference.")
    vendor_reference_ids = fields.One2many(
        'vendor.reference', 'purchase_order_id', string="Vendor References")
    bid_ids = fields.One2many('rfq.bid', 'rfq_id', string='Bids')

    # vendor_ids = fields.Many2many('res.partner', string='Vendors', domain=[('supplier_rank', '>', 0)])
