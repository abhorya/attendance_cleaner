{
    'name': 'Attendance Adjustment',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Adjust attendance records by removing duplicates and recording first check-in and last check-out.',
    'author': 'Sabry Youssef 01000059085 egypt',
    'website': 'https://sabry_youssef@me.com',
    'license': 'OPL-1',
    'price': 100.0,
    'currency': 'USD',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/attendance_actions_wizard_views.xml',
        'views/attendance_error_views.xml',
    ],
    'installable': True,
    'application': False,
}
