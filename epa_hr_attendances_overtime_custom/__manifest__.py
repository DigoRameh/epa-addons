# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Epa Hr Attendances Overtime Custom",
    "summary": """
        EPA HR Attendances Overtime Custom""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/epa-addons",
    "depends": [
        "hr_attendances_overtime",
        "hr_attendance_modification_tracking",
        "hr_attendance_reason",
        "hr_attendance_report_theoretical_time",
    ],
    "data": [
        "views/hr_attendance_sheet.xml",
        "views/hr_attendance_sheet_report.xml",
        "views/hr_attendance_sheet_template.xml",
        "views/hr_employee.xml",
        "security/epa_hr_attendances_overtime_custom_security.xml",
    ],
    "demo": [],
    "auto_install": True,
}
