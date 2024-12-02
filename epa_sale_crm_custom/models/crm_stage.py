# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class CrmStage(models.Model):

    _inherit = "crm.stage"

    validate_criteria_fields = fields.Boolean(
        string="Validate Criteria Fields",
        help="Requires all criteria fields filled when moving to this stage.",
    )
