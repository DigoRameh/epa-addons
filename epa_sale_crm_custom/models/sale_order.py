# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if "opportunity_id" in vals:
            opportunity_id = vals.get("opportunity_id")
            analytic_account_id = vals.get("analytic_account_id")

            # Verificar se já existe um nome
            if "name" not in vals or " / " not in vals["name"]:
                opportunity = self.env["crm.lead"].browse(opportunity_id)
                base_reference = opportunity.name

                existing_orders = self.env["sale.order"].search(
                    [
                        ("opportunity_id", "=", opportunity_id),
                        ("analytic_account_id", "=", analytic_account_id),
                    ]
                )

                sequential_numbers = []
                for existing_order in existing_orders:
                    parts = existing_order.name.split(" / ")
                    if len(parts) > 1 and parts[-1].isdigit():
                        sequential_numbers.append(int(parts[-1]))

                next_sequential = max(sequential_numbers, default=0) + 1

                vals["name"] = f"{base_reference} / {next_sequential}"

        else:
            if not self.env.user.has_group("sales_team.group_sale_manager"):
                raise UserError(
                    _(
                        "You cannot create a sale order without an opportunity. "
                        "Contact your sales administrator."
                    )
                )

        return super().create(vals)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.opportunity_id:
                all_orders = self.env["sale.order"].search(
                    [("opportunity_id", "=", order.opportunity_id.id)]
                )
                all_confirmed = all(o.state in ["sale", "done"] for o in all_orders)

                if all_confirmed:
                    order.opportunity_id.action_set_won()
        return res
