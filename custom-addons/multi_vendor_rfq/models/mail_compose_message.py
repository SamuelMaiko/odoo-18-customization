from odoo import models, api

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        # Ensuring the active_id and the model are correct
        if active_model == 'purchase.order' and active_id:
            order = self.env['purchase.order'].browse(active_id)

            # means it is still an rfq
            if order.state in ['draft', 'sent']:
                # Getting all vendor's email addresses
                partners = order.vendor_reference_ids.mapped('vendor_id').filtered(lambda p: p.email)
                res['partner_ids'] = [(6, 0, partners.ids)]  # Multiple vendors for RFQ

            # means it is a purchase order
            else:
                # getting the winning bidder's email stored in the partner id
                if order.partner_id and order.partner_id.email:
                    res['partner_ids'] = [(6, 0, [order.partner_id.id])]

        return res