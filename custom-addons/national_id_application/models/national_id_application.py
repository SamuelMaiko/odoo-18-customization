from odoo import models, fields, api
from zeep.xsd import DateTime


class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    _description = 'National ID Application'
    _inherit = ['mail.thread']

    name = fields.Char(string='Full Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    place_of_birth = fields.Char(string='Place of Birth', required=True)
    lc_reference_letter = fields.Binary(string='LC Reference Letter')
    picture = fields.Binary(string='Passport Photo')
    phone = fields.Char(string='Phone Number', required=True)
    email = fields.Char(string='Email', required=True)
    state = fields.Selection([
        ('stage1', 'Stage 1'),
        ('stage2', 'Stage 2'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='stage1', string='Stage', tracking=True)
    national_id_number = fields.Char(string='National ID Number')
    application_date = fields.Datetime(string='Application Date', default=fields.Datetime.now)
    date_approved = fields.Datetime(string='Approval Date')
    # used when the application has passed stage2
    can_reject_or_approve = fields.Boolean(string='Can Reject after stage 2', compute='_compute_can_reject_or_approve')

    def _compute_can_reject_or_approve(self):
        stage_1_group=self.env.ref('national_id_application.stage_1_approval_group')
        stage_2_group = self.env.ref('national_id_application.stage_2_approval_group')

        # check their group and state
        if stage_1_group in self.env.user.groups_id and self.state=='stage1':
            self.can_reject_or_approve = True
        elif stage_2_group in self.env.user.groups_id:
            self.can_reject_or_approve = True
        else:
            self.can_reject_or_approve = False

    def action_approve_stage_1(self):
        self.write({'state': 'stage2'})
        # preventing the stage approvers from getting an access error because approving moves it to stage2
        # which the record rules don't allow them to see the record anymore, so safe to redirect them back to the
        # list view
        stage_1_group = self.env.ref('national_id_application.stage_1_approval_group')
        if stage_1_group in self.env.user.groups_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'National ID Applications',
                'res_model': 'national.id.application',
                'view_mode': 'list,form',
                'target': 'current',
            }

        return True

    def action_approve_stage_2(self):
        self.write({'state': 'approved'})
        self.date_approved=fields.Datetime.now()
        # self.message_post(body="Stage 2 approved by user: %s" % self.env.user.name)

    def action_reject(self):
        self.write({'state': 'rejected'})
        # self.message_post(body="ID application rejected by user: %s" % self.env.user.name)
