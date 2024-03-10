# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class SportSport(models.Model):
    _name = 'sport.sport'
    _description = "Sport Sport"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
