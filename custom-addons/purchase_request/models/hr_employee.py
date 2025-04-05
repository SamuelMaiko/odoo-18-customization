from odoo import models, api

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        employee = super().create(vals)
        employee._check_and_assign_procurement_group()
        return employee

    def write(self, vals):
        res = super().write(vals)
        self._check_and_assign_procurement_group()
        return res

    def _check_and_assign_procurement_group(self):
        procurement_dept = self.env.ref('purchase_request.department_procurement', raise_if_not_found=False)
        procurement_group = self.env.ref('purchase_request.group_procurement_approver', raise_if_not_found=False)
        for employee in self:
            if procurement_dept and procurement_group and employee.department_id == procurement_dept:
                if procurement_group.id not in employee.user_id.groups_id.ids:
                    employee.user_id.write({'groups_id': [(4, procurement_group.id)]})
