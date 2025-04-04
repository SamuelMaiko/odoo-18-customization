from odoo import models, fields

class Task(models.Model):
    _name="task.task"
    _description="Task storing"

    name=fields.Char(string="Name", required=True)
    is_completed = fields.Boolean(string="Is Completed", default=False)