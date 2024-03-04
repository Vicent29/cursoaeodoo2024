# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models

class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = "Sport Player"

    name = fields.Char(string='Name', required=True)
    team_id = fields.Many2one('sport.team', string='Team')
    age = fields.Integer(string='Age')
    position = fields.Char(string='Position')
    starter = fields.Boolean(string='Starter')
    
    def action_make_starter(self):
        self.starter = True
    
    def action_make_substitute(self):
        self.starter = False
   