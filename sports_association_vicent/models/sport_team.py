# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api


class SportTeam(models.Model):
    _name = 'sport.team'
    _description = "Sport Team"

    name = fields.Char(string='Name', required=True)
    sport_id = fields.Many2one('sport.sport', string='Sport')
    player_ids = fields.One2many('sport.player', 'team_id', string='List Players')
    count_players = fields.Integer(string='Players',compute="_compute_count_players")
    logo = fields.Image(string='Logo')
    
    def action_make_all_starters(self):
        for record in self.player_ids:
            record.action_make_starter()
    
    def action_make_all_substitutes(self):
        for record in self.player_ids:
            record.action_make_substitute()
            
    @api.depends('player_ids')
    def _compute_count_players(self):
        for team in self:
            team.count_players = len(team.player_ids)
   