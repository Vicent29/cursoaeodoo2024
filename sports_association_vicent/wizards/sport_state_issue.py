# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api

class SportStateIssue(models.TransientModel):
    _name = 'sport.state.issue'
    _description = 'Change issue state to done'
    
    date = fields.Date('Date', default=fields.Date.today)    
    
    def change_state_done(self):
        active_ids = self.env.context.get('active_ids')
        # issues = self.env['sport.issue'].browse(active_ids)
        # issues = issues.filtered(lambda r: r.state != 'done')
        issues = self.env['sport.issue'].search([('id','in',active_ids),('state','!=','done')])
        issues.write({'date': self.date})
        issues.action_done()