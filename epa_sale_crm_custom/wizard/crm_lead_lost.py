# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class CrmLeadLost(models.TransientModel):
    _inherit = "crm.lead.lost"

    def action_lost_reason_apply(self):
        # Call the original method using super to keep the existing functionality
        res = super(CrmLeadLost, self).action_lost_reason_apply()

        # Get the leads from the active context
        leads = self.env["crm.lead"].browse(self.env.context.get("active_ids"))

        # Iterate over each lead to check for associated sale orders and cancel them
        for lead in leads:
            sale_orders = lead.order_ids
            for order in sale_orders:
                order.action_cancel()  # Cancel the sale order

        return res
