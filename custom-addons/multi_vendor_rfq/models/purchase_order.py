from odoo import models, fields, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_id = fields.Many2one(required=False)
    vendor_ids = fields.One2many('purchase.order.vendor', 'purchase_order_id', string="Vendors")
    bid_ids = fields.One2many("purchase.order.bid", "purchase_order_id", string="Bids")

    def button_confirm(self):
        """Override confirmation to require at least one vendor"""
        if not self.vendor_ids:
            raise UserError("You must specify at least one vendor")
        return super().button_confirm()

    def action_rfq_send(self):
        if not self.vendor_ids and self.state in ["draft", "sent"]:
            raise UserError(_("Please assign at least one vendor before sending."))

        # Determine the correct email template and recipient
        if self.state in ["draft", "sent"]:  # RFQ state
            template = self.env.ref("purchase.email_template_edi_purchase", raise_if_not_found=False)
            recipients = self.vendor_ids.mapped("vendor_id")  # Multiple vendors for RFQ
            default_email_to = ",".join(recipients.mapped("email"))  # All vendor emails for RFQ
        elif self.state in ["purchase"]:  # PO state
            template = self.env.ref("purchase.email_template_edi_purchase_done", raise_if_not_found=False)
            recipients = [self.partner_id]  # Only the selected vendor for PO
            default_email_to = self.partner_id.email if self.partner_id else None  # ✅ Only single vendor email for PO
        else:
            raise UserError(_("No suitable email template found for this document state."))

        if not template:
            raise UserError(_("Email template not found!"))

        if not recipients:
            raise UserError(_("No vendor has an email address!"))

        # Open the email sending wizard with the correct recipient(s)
        compose_form = self.env.ref("mail.email_compose_message_wizard_form", raise_if_not_found=False)
        ctx = {
            "default_model": "purchase.order",
            "default_res_ids": [self.id],  # Using list for multiple records
            "default_use_template": bool(template.id),
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "default_email_to": default_email_to,  # ✅ Only one vendor for PO
            # "default_partner_ids": recipients.ids,  # Needed for "Add contacts to notify"
        }

        return {
            "name": _("Send Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "target": "new",
            "context": ctx,
        }

    # def action_rfq_send(self):
    #     if not self.vendor_ids:
    #         raise UserError(_("Please assign at least one vendor before sending the RFQ."))
    #
    #     template = self.env.ref("purchase.email_template_edi_purchase", raise_if_not_found=False)
    #     if not template:
    #         raise UserError(_("Email template not found!"))
    #
    #     # Collect vendor partner records (not just emails)
    #     vendor_partners = self.vendor_ids.mapped("vendor_id")
    #
    #     if not vendor_partners:
    #         raise UserError(_("No vendor has an email address!"))
    #
    #     # Open the email sending wizard with pre-filled recipients
    #     compose_form = self.env.ref("mail.email_compose_message_wizard_form", raise_if_not_found=False)
    #     ctx = {
    #         "default_model": "purchase.order",
    #         "default_res_ids": [self.id],  # ✅ Updated to use 'default_res_ids' (list)
    #         "default_use_template": bool(template.id),
    #         "default_template_id": template.id,
    #         "default_composition_mode": "comment",
    #         "default_email_to": [vendor_partners.ids],
    #         "default_partner_ids": [vendor_partners.ids],  # ✅ Auto-filling vendors in "Recipients"
    #     }
    #
    #     return {
    #         "name": _("Send RFQ by Email"),
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "mail.compose.message",
    #         "views": [(compose_form.id, "form")],
    #         "target": "new",
    #         "context": ctx,
    #     }

