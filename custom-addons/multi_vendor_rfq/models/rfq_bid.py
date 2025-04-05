from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class RfqBid(models.Model):
    _name = 'rfq.bid'
    _description = 'RFQ Supplier Bid'

    rfq_id = fields.Many2one('purchase.order', string='Related RFQ', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier_rank', '>', 0)], required=True)
    bid_amount = fields.Float(string='Bid Amount')
    delivery_time = fields.Char(string='Proposed Delivery Time')
    selected = fields.Boolean(string="Selected", default=False)
    bid_status = fields.Selection(
        [("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        string="Bid Status",
        default="pending",
    )
    notes = fields.Text(string='Vendor Notes')

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
            if bid.selected and bid.rfq_id.bid_ids.filtered(lambda b: b.selected and b.id != bid.id):
                raise exceptions.ValidationError("Only one bid can be selected per RFQ.")

    def action_select_bid(self):
        # Marking this bid as selected and updating RFQ vendor.
        for bid in self:
            # unselecting all other bids and rejecting them
            bid.rfq_id.bid_ids.write({
                'selected': False,
                'bid_status': 'rejected'
            })
            # Selecting this bid and marking it as accepted
            bid.write({'selected': True, 'bid_status': 'accepted'})
            # assigning the vendor to the rfq
            bid.rfq_id.partner_id = bid.vendor_id
            # confirming the rfq, if not already done the ui
            bid.rfq_id.button_confirm()
            # setting the purchase order's amount equal to the accepted bid's price
            bid.rfq_id.amount_total = bid.bid_amount