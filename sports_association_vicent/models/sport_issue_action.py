# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class SportIssueAction(models.Model):
    _name = 'sport.issue.action'
    _description = "Sport Issue Action"

    name = fields.Char(string='Name', required=True)
    issue_id = fields.Many2one('sport.issue', string='Issue')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done')],
        string='State',
        default='draft',
    )
  