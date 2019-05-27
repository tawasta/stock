from odoo import models, api


class ProjectProject(models.Model):

    _inherit = 'project.project'

    @api.onchange('location_ids')
    @api.depends('location_ids')
    def _default_get_default_location(self):
        for record in self:
            if record.location_ids and not record.default_location_id:
                record.default_location_id = record.location_ids[0]
