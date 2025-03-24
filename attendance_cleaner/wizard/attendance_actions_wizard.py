from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class AttendanceCleanupWizard(models.TransientModel):
    _name = 'attendance.cleanup.wizard'
    _description = 'Attendance Cleanup Wizard'

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    confirm = fields.Boolean(string="Confirm Cleanup", required=True)
    error_messages = fields.Text(string="Messages", readonly=True)
    duplicate_count = fields.Integer(string="Duplicate Groups Found", compute='_compute_duplicate_count', store=False)

    @api.depends('date')
    def _compute_duplicate_count(self):
        for wizard in self:
            duplicate_groups = wizard.get_duplicate_groups()
            wizard.duplicate_count = len(duplicate_groups)

    def get_duplicate_groups(self):
        """
        Retrieve attendance records for the selected date, grouping them by employee and date.
        Only groups with more than one record are considered duplicates.
        """
        attendance_model = self.env['hr.attendance']
        selected_date = self.date or fields.Date.today()
        start_datetime = datetime.combine(selected_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)
        records = attendance_model.search([
            ('check_in', '>=', start_datetime),
            ('check_in', '<', end_datetime)
        ])
        groups = defaultdict(list)
        for record in records:
            if record.check_in:
                record_date = record.check_in.date()
                groups[(record.employee_id.id, record_date)].append(record)
        duplicate_groups = {key: recs for key, recs in groups.items() if len(recs) > 1}
        return duplicate_groups

    def check_attendance_errors(self):
        """
        Checks for duplicate attendance records on the selected date and displays a notification.
        """
        duplicate_groups = self.get_duplicate_groups()
        messages = []
        if duplicate_groups:
            messages.append(_("Found {} duplicate attendance group(s) for {}.").format(len(duplicate_groups), self.date))
            for (employee_id, rec_date), records in duplicate_groups.items():
                messages.append(_("Employee ID: {} on {} has {} records.").format(employee_id, rec_date, len(records)))
        else:
            messages.append(_("No duplicate attendance records found for {}.").format(self.date))
        self.error_messages = "\n".join(messages)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Attendance Check Result"),
                'message': self.error_messages,
                'type': 'info',
                'sticky': False,
            }
        }

    def preview_cleanup(self):
        """
        Provides a preview of the cleanup operation by listing what will be kept and which records will be removed.
        """
        duplicate_groups = self.get_duplicate_groups()
        preview_lines = []
        for (employee_id, rec_date), records in duplicate_groups.items():
            sorted_records = sorted(records, key=lambda r: r.check_in)
            if len(sorted_records) > 1:
                preview_lines.append(
                    _("Employee ID: {} on {} - Will keep record IDs: {} and {}; {} record(s) will be removed.").format(
                        employee_id,
                        rec_date,
                        sorted_records[0].id,
                        sorted_records[-1].id,
                        len(sorted_records) - 2
                    )
                )
        preview_message = "\n".join(preview_lines) if preview_lines else _("No records require cleanup for {}.").format(self.date)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Cleanup Preview"),
                'message': preview_message,
                'type': 'info',
                'sticky': False,
            }
        }

    def clean_attendance_records(self):
        """
        Cleans duplicate attendance records:
         - Groups records by employee and date.
         - If all records in a group share the same check-in/out times, it keeps the first and last records.
         - If times are inconsistent, it logs a warning and skips that group.
        """
        if not self.confirm:
            raise UserError(_("Please confirm the cleanup operation before proceeding."))

        attendance_model = self.env['hr.attendance']
        duplicate_groups = self.get_duplicate_groups()
        cleaned_groups = []
        error_groups = []

        for (employee_id, rec_date), records in duplicate_groups.items():
            sorted_records = sorted(records, key=lambda r: r.check_in)
            first_record = sorted_records[0]
            last_record = sorted_records[-1]

            # Verify consistency of check-in and check-out times in the group.
            consistent = all(
                rec.check_in == first_record.check_in and rec.check_out == last_record.check_out
                for rec in sorted_records
            )
            if not consistent:
                error_groups.append((employee_id, rec_date))
                _logger.warning("Inconsistent attendance times for employee %s on %s.", employee_id, rec_date)
                continue

            if len(sorted_records) > 2:
                record_ids_to_delete = [rec.id for rec in sorted_records[1:-1]]
                attendance_model.browse(record_ids_to_delete).unlink()
                _logger.info("Deleted %s duplicate attendance records for employee %s on %s.",
                             len(record_ids_to_delete), employee_id, rec_date)

            if first_record.check_out != last_record.check_out:
                first_record.write({'check_out': last_record.check_out})
            cleaned_groups.append((employee_id, rec_date))

        if error_groups:
            error_message = _("The following groups had inconsistent check-in/check-out times and were not cleaned:\n")
            for emp, dt in error_groups:
                error_message += _("Employee ID: {} on {}\n").format(emp, dt)
            self.error_messages = error_message
            raise UserError(self.error_messages)

        success_message = _("Cleanup completed successfully for {} duplicate group(s) on {}.").format(len(cleaned_groups), self.date)
        self.error_messages = success_message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Cleanup Result"),
                'message': self.error_messages,
                'type': 'success',
                'sticky': False,
            }
        }
