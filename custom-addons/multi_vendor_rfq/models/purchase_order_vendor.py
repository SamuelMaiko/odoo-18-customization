from odoo import models, fields

class PurchaseOrderVendor(models.Model):
    _name = "purchase.order.vendor"
    _description = "RFQ Vendor Mapping"

    purchase_order_id = fields.Many2one("purchase.order", string="RFQ", required=True, ondelete="cascade")
    vendor_id = fields.Many2one("res.partner", string="Vendor", required=True, domain=[("supplier_rank", ">", 0)])
    status = fields.Selection([
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ], string="Status", default="pending")