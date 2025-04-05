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

    # Actions
    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})
    # creating a new rfq

