from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _description = "Purchase Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Request Reference", required=True, copy=False, default="New")
    employee_id = fields.Many2one("hr.employee", string="Requested By", required=True, default=lambda self: self.env.user)
    date_request = fields.Date(string="Request Date", required=True, default=fields.Date.today)
    department_id = fields.Many2one("hr.department", string="Department", required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rfq_created", "RFQ Created"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    line_ids = fields.One2many("purchase.request.line", "request_id", string="Purchase Items")

    def action_submit(self):
        """Submit request for approval."""
        self.state = "submitted"

    def action_approve(self):
        """Approve the request."""
        self.state = "approved"

    def action_create_rfq(self):
        """Create an RFQ from the request."""
        purchase_order = self.env["purchase.order"].create({
            "partner_id": self.env.ref("base.res_partner_1").id,
            "order_line": [(0, 0, {
                "product_id": line.product_id.id,
                "product_qty": line.quantity,
                "price_unit": line.product_id.list_price,
            }) for line in self.line_ids]
        })
        self.state = "rfq_created"
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": purchase_order.id,
        }

class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _description = "Purchase Request Line"

    request_id = fields.Many2one("purchase.request", string="Purchase Request", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1)
