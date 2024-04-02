from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class WorkOrder(models.Model):
    _name = 'work.order'

    name = fields.Char(string='WO Number', readonly=True, default='/')
    sale_id = fields.Many2one('sale.order', string="Booking Order Reference", domain=[('is_booking_order', '=', True)])
    service_team_id = fields.Many2one('service.team', string='Team')
    team_leader_id = fields.Many2one('res.users', related="service_team_id.team_leader_id")
    team_member_ids = fields.Many2many('res.users', related="service_team_id.team_member_ids")
    planned_start = fields.Datetime(string="Planned Start", required=True)
    planned_end = fields.Datetime(string="Planned End", required=True)
    date_start = fields.Datetime(string="Date Start", readonly=True)
    date_end = fields.Datetime(string="Date End", readonly=True)
    state = fields.Selection(
        [("pending", "Pending"), ("in_progress", "In Progress"),("done", "Done"),("cancelled", "Cancelled")], 
        string="Journal Type",
        default='pending'
    )
    notes = fields.Text()

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if vals.get('name', _('/')) == _('/'):
                if 'company_id' in vals:
                    vals['name'] = self.env['ir.sequence'].with_company(vals['company_id']).next_by_code('work.order') or _('/')
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code('work.order') or _('/')

        return super(WorkOrder, self).create(values)
    
    def start_wo(self):
        self.write({
            'state': 'in_progress',
            'date_start': fields.Datetime.now()
        })
    def end_wo(self):
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now()
        })
    def reset_wo(self):
        self.write({
            'state': 'pending',
            'date_start': False
        })
    def cancel_wo(self):
        return {    
            'name': _("Reason For Cancellation"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cancel.work.order',
            'view_id': self.env.ref('booking_order_erik_firmansyah_02042024.cancel_work_order_wizard_views').id,
            'target': 'new',
            'context': {
                'default_work_order_id': self.id,
            }
        }



