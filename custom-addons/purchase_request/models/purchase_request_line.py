from odoo import models, fields, api

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    date_required = fields.Date(string='Date Needed')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')
    # unit_price = fields.Float(string='Unit Price')
    # total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    sequence = fields.Integer(string='Sequence', default=10)

    # actions
    def approve_line(self):
        for line in self:
            line.state = 'approved'

    def reject_line(self):
        for line in self:
            line.state = 'rejected'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.standard_price

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.description = line.product_id.name

