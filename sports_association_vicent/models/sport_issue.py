# Copyright 2024 Vicent Esteve - vesteve@ontinet.com
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _

class SportIssue(models.Model):
    _name = 'sport.issue'
    _description = "Sport Issue"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.today)
    assistance = fields.Boolean(string='Assistante', help='Show if the isuue has asssitence')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done')],
        string='State',
        default='draft',
    )
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    sequence = fields.Integer(string='Sequence', default=10)
    solution = fields.Html('Solution')
    color = fields.Integer(string ='color', default=0)
    assigned = fields.Boolean(string='Assigned',compute="_compute_assigned",inverse="_inverse_assigned", search="_search_assigned")
    
    clinic_id = fields.Many2one('sport.clinic', string='Clinic')
    player_id = fields.Many2one('sport.player', string='Player')
    tag_ids = fields.Many2many('sport.issue.tag', string='Tags')
    cost = fields.Float(string='cost')
    
    action_ids = fields.One2many('sport.issue.action', 'issue_id', string='Actions to do')
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name of the issue must be unique.'),
    ]
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.name:
                existing_issue = self.search([('name', '=', record.name), ('id', '!=', record.id)])
                if existing_issue:
                    raise ValidationError("The name of the issue must be unique.")
    
    @api.constrains('cost')
    def _check_cost(self):
        for record in self:
            if record.cost < 0:
                raise ValidationError(_("The cost cannot be negative."))
    
    @api.onchange('clinic_id')
    def _onchange_clinic(self):
        for record in self:
            if record.clinic_id:
                record.assistance = True

    def action_open(self):
        # import pdb:pdb.set_trace() --> para hacer como un debug o punto de interrupción
        # self.ensure_one() --> COmprobar que solo haya uno objecto en el self 
        # self.write({'state': 'open'}) -->Tambien sirve como bucle
        for record in self:
            record.state= 'open'
            
    def action_draft(self):
        for record in self:
            if not record.date:
                raise UserError(_('The date is required'))
        record.state= 'draft'
            
    def action_done(self):
        for record in self:
            record.state= 'done'         
        
    def action_open_all_issues(self):
        issues = self.env['sport.issue'].search([]) #Guardara todas las incidencias
        issues.action_open() #Llamrara al metodo de action_open
    
    def _compute_assigned(self):
        for record in self:
            record.assigned = bool(record.user_id)

    def _inverse_assigned(self):
        for record in self:
            if not record.user_id:
                record.assigned = False
            else:    
                record.assigned = True
    
    def _search_assigned(self, operator, value):
        for record in self:
            if operator == "=":
                return[('user_id', operator, value)]
            else:    
                return[]
    
    def action_add_tags(self):
        for record in self:
            # import pdb; pdb.set_trace()
            tag_ids = self.env['sport.issue.tag'].search([('name', 'like', record.name)])
            if tag_ids:
                record.tag_ids = [(6, 0, tag_ids.ids)]
            else:
                new_tag_issue = self.env['sport.issue.tag'].create({'name': record.name})
                record.tag_ids = [(6, 0, new_tag_issue.id.ids)]
                
    def _cron_delete_unused_tags(self):
        tag_ids = self.env['sport.issue.tag'].search([])
        for tag in tag_ids:
            issue = self.env['sport.issue'].search([('tag_ids', 'in', tag.id)])
            if not issue:
                tag.unlink()
