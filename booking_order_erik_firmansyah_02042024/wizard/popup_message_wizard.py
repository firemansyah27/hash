from odoo import api, fields, models 

class PopupMessage(models.TransientModel):
    _name = 'popup.message'
    _description = 'Popup Message Wizard'

    message = fields.Char()