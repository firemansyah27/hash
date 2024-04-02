from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from collections import namedtuple


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean()
    service_team_id = fields.Many2one('service.team', string='Team')
    team_leader_id = fields.Many2one('res.users', related="service_team_id.team_leader_id")
    team_member_ids = fields.Many2many('res.users', related="service_team_id.team_member_ids")
    booking_start = fields.Datetime(string="Booking Start")
    booking_end = fields.Datetime(string="Booking End")
    work_order_ids = fields.Many2many('work.order', 'sale_order_work_order_rel', compute="_get_work_order", string="Work Orders")
    work_order_count = fields.Integer(compute="_get_work_order")

    def _check_team(self):
        for rec in self:
            active_work_order_ids = self.env['work.order'].search([('state', '=', 'in_progress')])
            for active_work_order_id in active_work_order_ids:
                Range = namedtuple('Range', ['start', 'end'])
                r1 = Range(start=rec.booking_start, end=rec.booking_end)
                r2 = Range(start=active_work_order_id.planned_start, end=active_work_order_id.planned_end)
                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days + 1
                overlap = max(0, delta)
                if overlap > 0:
                    return True, 'Team already has work order during that period on {}'.format(active_work_order_id.sale_id.name)
            
            return False, 'Team is available for booking'
    
    def check_team(self):
        _ , message = self._check_team()
        return self.popup_message(message)


    def popup_message(self, message):
        return {    
            'name': _("Check Result"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'popup.message',
            'view_id': self.env.ref('booking_order_erik_firmansyah_02042024.popup_message_wizard_views').id,
            'target': 'new',
            'context': {
                'default_message': message,
            }
        }
    
    def action_confirm(self):
        is_overlap , message = self._check_team()

        if is_overlap:
            return self.popup_message(message)
        else:
            WO = self.env['work.order']
            WO.create({
                'sale_id': self.id,
                'service_team_id': self.service_team_id.id,
                'planned_start': self.booking_start,
                'planned_end': self.booking_end,
            })
        res = super(SaleOrder, self).action_confirm()
        return res
    
    def _get_work_order(self):
        for rec in self:
            work_orders = self.env['work.order'].search([('sale_id', '=', rec.id)])
            if work_orders:
                rec.work_order_ids = work_orders
                rec.work_order_count = len(work_orders)
            else:
                rec.work_order_count = 0
    
    def action_view_work_order(self):
        return self._get_action_view_work_order(self.work_order_ids)

    def _get_action_view_work_order(self, work_order_ids):
        action = self.env["ir.actions.actions"]._for_xml_id("booking_order_erik_firmansyah_02042024.action_work_order")
        if len(work_order_ids) > 1:
            action['domain'] = [('id', 'in', work_order_ids.ids)]
        elif work_order_ids:
            form_view = [(self.env.ref('booking_order_erik_firmansyah_02042024.work_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = work_order_ids.id
        return action