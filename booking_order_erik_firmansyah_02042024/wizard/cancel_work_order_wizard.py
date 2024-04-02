from odoo import api, fields, models 

class CancelWorkOrder(models.TransientModel):
    _name = 'cancel.work.order'
    _description = 'Cancel Work Wizard'

    work_order_id = fields.Many2one('work.order')
    message = fields.Text(string='Reason')

    def action_cancel(self):
        for rec in self:
            rec.work_order_id.write({
                'state': 'cancelled',
                'notes': self.message,
            })
