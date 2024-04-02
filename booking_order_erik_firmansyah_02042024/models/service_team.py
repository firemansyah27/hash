from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ServiceTeam(models.Model):
    _name = 'service.team'

    name = fields.Char('Team Name', required=True)
    team_leader_id = fields.Many2one('res.users', required=True)
    team_member_ids = fields.Many2many('res.users')