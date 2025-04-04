from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class PurchaseOrderBid(models.Model):
    _name = "purchase.order.bid"
    _description = "RFQ Bids"

    purchase_order_id = fields.Many2one(
        "purchase.order", string="RFQ", required=True, ondelete="cascade"
    )
    vendor_id = fields.Many2one(
        "res.partner", string="Vendor", required=True, domain=[("supplier_rank", ">", 0)]
    )
    bid_status = fields.Selection(
        [("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        string="Bid Status",
        default="pending",
    )
    notes = fields.Text(string="Notes")
    price = fields.Float(string="Bid Price", required=True)
    selected = fields.Boolean(string="Selected", default=False)

    _sql_constraints = [
        (
            "unique_vendor_bid",
            "unique(purchase_order_id, vendor_id)",
            "Each vendor can submit only one bid per RFQ!",
        )
    ]

    @api.constrains('selected')
    def _check_unique_selected(self):
        # Ensuring only one bid is selected per RFQ.
        for bid in self:
            if bid.selected and bid.purchase_order_id.bid_ids.filtered(lambda b: b.selected and b.id != bid.id):
                raise exceptions.ValidationError("Only one bid can be selected per RFQ.")

    def action_select_bid(self):
        # Marking this bid as selected and updating RFQ vendor.
        for bid in self:
            # unselecting all other bids and rejecting them
            bid             .purchase_order_id.bid_ids.write({
                'selected': False,
                'bid_status': 'rejected'
            })
            # Selecting this bid and marking it as accepted
            bid.write({'selected': True, 'bid_status': 'accepted'})
            # assigning the vendor to the rfq
            bid.purchase_order_id.partner_id = bid.vendor_id
            # confirming the rfq, if not already done the ui
            bid.purchase_order_id.button_confirm()
            #setting the purchase order's amount equal to the accepted bid's price
            bid.purchase_order_id.amount_total = bid.price

