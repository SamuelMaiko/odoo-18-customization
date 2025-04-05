from odoo import models, api

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model')
        print("ACTIVE MODEL",active_model)
        active_id = self.env.context.get('active_id')

        if active_model == 'purchase.order' and active_id:
            order = self.env['purchase.order'].browse(active_id)
            print("ACTIVE ID", order)

            if order.vendor_reference_ids:
                partners = order.vendor_reference_ids.mapped('vendor_id').filtered(lambda p: p.email)
                print("VENDORS", partners)
                res['partner_ids'] = [(6, 0, partners.ids)]

        return res