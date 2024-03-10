# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api

class SportLeague(models.Model):
    _name = 'sport.league'
    _description = 'Sport League'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    sport_id = fields.Many2one('sport.sport', string='Sport')
    sport_league_ids = fields.One2many('sport.league.line', 'league_id', string='League Lines')

    def set_score(self):
        for record in self.sport_league_ids:
            team = record.team_id
            score_points = self.env['sport.match'].search([('sport_id', '=', self.sport_id.id), ('winner_team_id', '=', team.id)]).mapped('score_winning')
            record.points = sum(score_points)

class SportLeagueLine(models.Model):
    _name = 'sport.league.line'
    _description = 'Sport League Line'
    _order = 'points desc'

    league_id = fields.Many2one('sport.league', string='League')
    team_id = fields.Many2one('sport.team', string='Team')
    points = fields.Integer('Points')