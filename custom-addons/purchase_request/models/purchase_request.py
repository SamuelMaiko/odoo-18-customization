from odoo import models, fields, api, _


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string='Request Name', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id',
                                    readonly=True)
    product_ids = fields.One2many('purchase.request.line', 'request_id', string='Requested Products')
    date_requested = fields.Date(string='Date Requested', default=fields.Date.today, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    rfq_id = fields.Many2one('purchase.order', string='Related RFQ', readonly=True)

    # Actions
    def action_approve(self):
        self.write({'state': 'approved'})
        self.create_rfq()

    def action_reject(self):
        self.write({'state': 'rejected'})

    def create_rfq(self):
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.env.ref('base.main_company').id,
            'date_order': fields.Date.today(),
            'state': 'draft',
            'origin': self.name,
        })

        # Iterating through the products requested to add to the rfq
        for request_line in self.product_ids:
            self.env['purchase.order.line'].create({
                'order_id': purchase_order.id,
                'product_id': request_line.product_id.id,
                'product_qty': request_line.quantity,
                'price_unit': request_line.unit_price,
                'name': request_line.product_id.name,
            })

