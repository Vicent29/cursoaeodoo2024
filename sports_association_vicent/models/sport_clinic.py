# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api


class SportClinic(models.Model):
    _name = 'sport.clinic'
    _description = "Sport Clinic"

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    issue_ids = fields.One2many('sport.issue', 'clinic_id', string='Issues')
    available = fields.Boolean(string='Available')
    issue_count = fields.Integer('Issue_count', compute="_compute_issue_count")
    
    def action_check_assistance(self):
        for record in self.issue_ids:
            record.assistance = True
    
    
    #Samrthbutton
    def action_view_issues(self):
        return {
            'name': 'Issues',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.issue',
            'view_mode': 'tree,form',
            'domain': [('clinic_id', '=', self.id)]
        }
        
    @api.depends('issue_ids')
    def _compute_issue_count(self):
        for record in self:
            record.issue_count = len(record.issue_ids)
        