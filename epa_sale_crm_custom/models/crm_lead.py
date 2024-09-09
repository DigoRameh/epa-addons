# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # Overwrite name to set readonly
    name = fields.Char(
        required=False,
        readonly=True,
    )
    # Other fields
    alias_name = fields.Char(
        string="Codename",
        required=True,
    )
    interesting_client = fields.Boolean(string="Interesting Client")
    appropriate_equipment = fields.Boolean(string="Appropriate Equipment")
    adequate_documentation = fields.Boolean(string="Adequate Documentation")
    validated_methodologies = fields.Boolean(string="Validated Methodologies")
    available_labor = fields.Boolean(string="Available Labor")
    qualified_labor = fields.Boolean(string="Qualified Labor")
    completion_period = fields.Boolean(string="Feasible Completion Period")
    payment_term = fields.Boolean(string="Adequate Payment Term")
    operational_viability = fields.Boolean(string="Operational Viability")
    financial_viability = fields.Boolean(string="Financial Viability")
    client_financial_health = fields.Boolean(string="Client Adequate Financial Health")
    client_cash_flow = fields.Boolean(string="We Serve Client Cash Flow")
    technological_risks = fields.Boolean(string="Acceptable Technological Risks")
    legal_risks = fields.Boolean(string="Acceptable Legal Risks")
    political_risks = fields.Boolean(string="Acceptable Political Risks")
    subcontracting_possibility = fields.Boolean(string="Subcontracting Possibility")
    subcontracting_laboratory = fields.Boolean(string="Laboratory")
    subcontracting_probe = fields.Boolean(string="Probe")
    subcontracting_sampling = fields.Boolean(string="Sampling")
    subcontracting_others = fields.Char(string="Others")
    proposal_date = fields.Date(string="Proposal Date")
    group_companies = fields.Many2one("res.company", string="Group Companies")
    company_contacts = fields.Many2one("res.partner", string="Company Contacts")
    type_id = fields.Many2one(
        comodel_name="project.type",
        string="Type",
        copy=False,
        domain="[('project_ok', '=', True)]",
        required=True,
    )
    project_manager = fields.Many2one(related="team_id", string="Project Manager")
    quotation_analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account for Quotation",
    )

    @api.model
    def create(self, vals):
        if "name" not in vals or not vals["name"]:
            vals["name"] = self.env["ir.sequence"].next_by_code("crm.lead") or "/"
        if "alias_name" in vals:
            vals["name"] = f"{vals['name']} | {vals['alias_name']}"
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for lead in self:
            if "stage_id" in vals:
                new_stage = self.env["crm.stage"].browse(vals["stage_id"])
                if new_stage.validate_criteria_fields:
                    criteria_fields = [
                        "interesting_client",
                        "appropriate_equipment",
                        "adequate_documentation",
                        "validated_methodologies",
                        "available_labor",
                        "qualified_labor",
                        "completion_period",
                        "payment_term",
                        "operational_viability",
                        "financial_viability",
                        "client_financial_health",
                        "client_cash_flow",
                        "technological_risks",
                        "legal_risks",
                        "political_risks",
                    ]
                    missing_fields = []
                    for field_name in criteria_fields:
                        field_value = getattr(lead, field_name)
                        if not field_value:
                            field_label = lead._fields[field_name].string
                            missing_fields.append(field_label)
                    if missing_fields:
                        raise ValidationError(
                            _(
                                'Cannot move to stage "{}". Missing fields:\n\n{}'
                            ).format(
                                new_stage.name,
                                "\n".join(missing_fields),
                            )
                        )
            if "alias_name" in vals:
                if lead.name:
                    lead.name = f"{lead.name.split(' | ')[0]} | {vals['alias_name']}"
        return res

    def action_new_quotation(self):
        if not self.quotation_analytic_account_id:
            return {
                "type": "ir.actions.act_window",
                "res_model": "crm.lead.analytic.account.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_lead_id": self.id,
                },
            }
        res = super().action_new_quotation()
        res["context"][
            "default_analytic_account_id"
        ] = self.quotation_analytic_account_id.id
        return res

    @api.onchange("subcontracting_possibility")
    def _onchange_subcontracting_possibility(self):
        if not self.subcontracting_possibility:
            self._reset_subcontracting_fields()

    def _reset_subcontracting_fields(self):
        self.subcontracting_laboratory = False
        self.subcontracting_probe = False
        self.subcontracting_sampling = False
        self.subcontracting_others = ""
