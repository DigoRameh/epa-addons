# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "EPA Sale CRM Custom",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/epa-addons",
    "depends": ["sale_crm", "project_category"],
    "data": [
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/crm_stage.xml",
        "views/crm_lead.xml",
        "wizard/crm_lead_analytic_account_wizard.xml",
    ],
}
