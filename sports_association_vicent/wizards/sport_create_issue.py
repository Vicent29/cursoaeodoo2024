# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api

class SportCreateIssue(models.TransientModel):
    _name = 'sport.create.issue'
    _description = 'Create Issue'
    
    name = fields.Char('Issue name')
    # clinic_id = fields.Many2one('sport.clinic', string='Clinic', default=lambda self: self.env.context.get('active_id'))  # CLINICA POR DEFECTO
    clinic_id = fields.Many2one('sport.clinic', string='Clinic')
    player_id = fields.Many2one('sport.player', string='Player')

    
    def create_issue(self):
        modelFrom = self.env.context.get('active_model')
        if (modelFrom == 'sport.clinic'):
            clinic = self.env[modelFrom].browse(self.env.context.get('active_id'))
            vals = {
                'name': self.name,
                'clinic_id': clinic.id,
                'player_id': self.player_id.id
            }
        elif ( modelFrom == 'sport.player'):
            player = self.env[modelFrom].browse(self.env.context.get('active_id'))
            vals = {
                'name': self.name,
                'clinic_id': self.clinic_id.id,
                'player_id': player.id
            }
        issue = self.env['sport.issue'].create(vals)
        return {
            'name': 'Issue',
            'view_mode': 'form',
            'res_model': 'sport.issue',
            'res_id': issue.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }