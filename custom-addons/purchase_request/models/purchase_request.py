from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _inherit = ['mail.thread']
    _description = 'Purchase Request'

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, index=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id',
                                    readonly=True)
    product_ids = fields.One2many('purchase.request.line', 'request_id', string='Requested Products')
    date_requested = fields.Date(string='Date Requested', default=fields.Date.today, required=True,readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    rfq_id = fields.Many2one('purchase.order', string='Related RFQ', readonly=True)
    has_approved_product = fields.Boolean(compute='_compute_has_approved_product', store=False)
    can_edit_lines = fields.Boolean(compute="_compute_can_edit_lines")

    def _compute_can_edit_lines(self):
        for record in self:
            record.can_edit_lines = (
                    record.state != 'approved'
                    or self.env.user.has_group('purchase_request.group_procurement_approver')
            )

    @api.depends('product_ids.state')
    def _compute_has_approved_product(self):
        for rec in self:
            rec.has_approved_product = any(line.state == 'approved' for line in rec.product_ids)


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        return super(PurchaseRequest, self).create(vals)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee:
            res['employee_id'] = employee.id
        return res
    # Actions
    def action_create_rfq(self):
        if not self.env.user.has_group('purchase_request.group_procurement_approver'):
            raise AccessError("Only procurement employees can create rfqs for purchase requests.")

        if not self.has_approved_product:
            raise ValidationError("At least one product must be approved.")
        purchase_order = self.env['purchase.order'].create({
            'partner_id': False,
            'date_order': fields.Date.today(),
            'state': 'draft',
            'origin': self.name,
        })

        # Iterating through the products requested to add to the rfq
        for request_line in self.product_ids:
            if request_line.state == 'approved':
                self.env['purchase.order.line'].create({
                    'order_id': purchase_order.id,
                    'product_id': request_line.product_id.id,
                    'product_qty': request_line.quantity,
                    'name': request_line.product_id.name,
                })
        # updating the related rfq and the state
        self.write({
            'rfq_id': purchase_order.id,
            'state': 'approved'
        })

    def action_update_related_rfq(self):
        if not self.env.user.has_group('purchase_request.group_procurement_approver'):
            raise AccessError("Only procurement employees can update rfqs purchase requests.")

        related_rfq=self.env['purchase.order'].browse(self.rfq_id.id)

        related_rfq.order_line.unlink()

        for request_line in self.product_ids:
            if request_line.state == 'approved':
                self.env['purchase.order.line'].create({
                    'order_id':related_rfq.id,
                    'product_id':request_line.product_id.id,
                    'product_qty': request_line.quantity,
                    'name': request_line.product_id.name,
                })
        self.write({'state': 'approved'})

    def action_reject(self):
        if not self.env.user.has_group('purchase_request.group_procurement_approver'):
            raise AccessError("Only procurement employees can reject purchase requests.")
        # purchase request state
        self.write({'state': 'rejected'})
        # rejecting all products in the purchase request
        self.product_ids.write({'state':'rejected'})

        #updating the rfq to remove the products
        self.action_update_related_rfq()

    @api.constrains('product_ids')
    def _check_product_ids(self):
        for rec in self:
            if not rec.product_ids:
                raise ValidationError("At least one product must be requested.")



# TO DO
# prevent the requesters from editing after approved - Done
# look at api.model ...... methods
# guiding messages