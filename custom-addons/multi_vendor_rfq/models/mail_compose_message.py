from odoo import models, api

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        # Ensure active_id and model are correct before proceeding
        if active_model == 'purchase.order' and active_id:
            order = self.env['purchase.order'].browse(active_id)

            # For RFQ (state = 'draft' or 'sent'), populate all vendor emails
            if order.state in ['draft', 'sent']:
                # Get all vendor email addresses (multiple vendors in RFQ)
                partners = order.vendor_reference_ids.mapped('vendor_id').filtered(lambda p: p.email)
                res['partner_ids'] = [(6, 0, partners.ids)]  # Multiple vendors for RFQ

            # elif order.state == 'purchase'
            else:
                # Get the selected vendor's email (single vendor for PO)
                if order.partner_id and order.partner_id.email:
                    res['partner_ids'] = [(6, 0, [order.partner_id.id])]  # Single vendor for PO

        return res