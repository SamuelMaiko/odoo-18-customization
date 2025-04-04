from odoo import models, api
from odoo.tools import email_normalize


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        """
        Override send action to:
        1. First send to main vendor (original behavior)
        2. Then send RFQs to all other vendors
        """
        if self._context.get('custom_rfq_mode'):
            # Get the original purchase order
            order = self.env['purchase.order'].browse(self._context.get('active_id'))

            # 1. First send to main vendor (original behavior)
            res = super().action_send_mail()

            # 2. Prepare RFQ emails for other vendors
            vendor_ids = self._context.get('vendor_ids', [])
            main_vendor = order.partner_id.id

            for vendor_id in vendor_ids:
                if vendor_id != main_vendor:
                    # Create new composer for each vendor
                    vendor = self.env['res.partner'].browse(vendor_id)
                    if email_normalize(vendor.email):
                        self.copy({
                            'partner_ids': [(6, 0, [vendor_id])],
                            'subject': f"RFQ: {order.name}",
                            'body': f"Dear {vendor.name},<br/><br/>"
                                    f"Please find attached the RFQ for your review.<br/><br/>"
                                    f"Best regards,<br/>{self.env.user.company_id.name}",
                            'email_from': self.env.user.email_formatted,
                        }).action_send_mail()

            return res

        return super().action_send_mail()