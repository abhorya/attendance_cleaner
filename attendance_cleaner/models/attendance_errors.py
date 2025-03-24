# models/attendance_error.py
from odoo import models, fields

class AttendanceError(models.Model):
    _name = 'attendance.error'
    _description = 'Attendance Error'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    error_type = fields.Selection([
        ('duplicate_check_in', 'Duplicate Check-In'),
        ('duplicate_check_out', 'Duplicate Check-Out'),
    ], string="Error Type", required=True)
    error_date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description")

    def action_save(self):
        # Implement the logic for saving the error or handling it
        pass
