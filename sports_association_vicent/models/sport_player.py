# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api
from datetime import date

class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = "Sport Player"

    name = fields.Char(string='Name', required=True)
    team_id = fields.Many2one('sport.team', string='Team')
    age = fields.Integer(string='Age',compute='_compute_age', store=True)
    birth_date = fields.Date(string='Birthdate')
    position = fields.Char(string='Position')
    starter = fields.Boolean(string='Starter', default=True)
    sport_name = fields.Char(string="Sport",related='team_id.sport_id.name', store=True)
    
    def action_make_starter(self):
        self.starter = True
    
    def action_make_substitute(self):
        self.starter = False
    
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))

    # Añadir un botón en los equipos que busque los jugadores que no tengan equipo, menores de 30 años, y los añada al equipo.