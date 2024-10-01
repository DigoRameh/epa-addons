# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    attendance_sheet_ids = fields.Many2many(
        comodel_name="hr.attendance.sheet",
        string="Employee Attendance Sheets",
        compute="_compute_attendance_sheet_ids",
        readonly=True,
    )
    leave_ids = fields.Many2many(
        comodel_name="hr.leave",
        string="Employee Leaves",
        compute="_compute_leave_ids",
        readonly=True,
    )
    total_overtime = fields.Float(
        string="Total Overtime",
        compute="_compute_times",
        readonly=True,
    )
    total_difftime = fields.Float(
        string="Total Difftime",
        compute="_compute_times",
        readonly=True,
    )
    time_bank = fields.Float(
        string="Time Bank",
        compute="_compute_times",
        readonly=True,
    )
    total_leave_time = fields.Float(
        string="Total Leave Time",
        compute="_compute_times",
        readonly=True,
    )
    time_bank_real = fields.Float(
        string="Time Bank Real",
        compute="_compute_times",
        readonly=True,
    )

    @api.depends()
    def _compute_attendance_sheet_ids(self):
        for employee in self:
            employee.attendance_sheet_ids = self.env["hr.attendance.sheet"].search(
                [("employee_id", "=", employee.id)],
            )

    @api.depends()
    def _compute_leave_ids(self):
        for employee in self:
            employee.leave_ids = self.env["hr.leave"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("state", "in", ["validate", "validate1"]),
                ],
            )

    @api.depends("attendance_sheet_ids", "leave_ids")
    def _compute_times(self):
        for employee in self:
            employee.total_overtime = sum(
                employee.attendance_sheet_ids.mapped("total_overtime")
            )
            employee.total_difftime = sum(
                employee.attendance_sheet_ids.mapped("total_difftime")
            )
            employee.time_bank = employee.total_overtime - employee.total_difftime
            employee.total_leave_time = sum(
                employee.leave_ids.mapped("number_of_hours_display")
            )
            employee.time_bank_real = employee.time_bank - employee.total_leave_time

    def action_view_attendances(self):
        self.ensure_one()
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "hr_attendances_overtime.action_attendance_sheets1"
        )
        result["domain"] = [("id", "in", self.attendance_sheet_ids.ids)]
        return result
