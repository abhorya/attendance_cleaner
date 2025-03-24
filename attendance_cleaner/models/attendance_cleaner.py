# models/attendance_wizard.py
from odoo import models, fields, api

class AttendanceCleanupWizard(models.TransientModel):
    _name = 'attendance.cleanup.wizard'
    _description = 'Attendance Cleanup Wizard'

    confirm = fields.Boolean(string="Confirm Cleanup", required=True)
    error_messages = fields.Text(string="Errors", readonly=True)

    def check_attendance_errors(self):
        attendance_model = self.env['hr.attendance']
        attendance_records = attendance_model.search([])

        errors = []
        attendance_dict = {}

        for record in attendance_records:
            key = (record.employee_id.id, record.check_in.date())
            if key not in attendance_dict:
                attendance_dict[key] = {
                    'check_ins': [],
                    'check_outs': [],
                }
            attendance_dict[key]['check_ins'].append(record.check_in)
            attendance_dict[key]['check_outs'].append(record.check_out)

        # Clear previous errors
        self.env['attendance.error'].search([]).unlink()

        for key, value in attendance_dict.items():
            if len(value['check_ins']) > 1:
                error_description = f"Duplicate check-ins for employee ID {key[0]} on {key[1]}."
                errors.append(error_description)
                self.env['attendance.error'].create({
                    'employee_id': key[0],
                    'error_type': 'duplicate_check_in',
                    'error_date': key[1],
                    'description': error_description,
                })
            if len(value['check_outs']) > 1:
                error_description = f"Duplicate check-outs for employee ID {key[0]} on {key[1]}."
                errors.append(error_description)
                self.env['attendance.error'].create({
                    'employee_id': key[0],
                    'error_type': 'duplicate_check_out',
                    'error_date': key[1],
                    'description': error_description,
                })

        if errors:
            self.error_messages = "Errors found:\n" + "\n".join(errors)
        else:
            self.error_messages = "No errors found."

    def clean_attendance_records(self):
        if not self.confirm:
            return

        # Call the method to clean attendance records
        attendance_model = self.env['hr.attendance']
        attendance_model.clean_attendance_records()
