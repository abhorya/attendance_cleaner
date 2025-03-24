# Attendance Cleaner

The **Attendance Cleaner** module is designed to help Odoo administrators and HR teams maintain data integrity in attendance records. It identifies and cleans up duplicate attendance records for a selected date by grouping records by employee and date, previewing potential changes, and safely merging duplicates.

## Features

- **Duplicate Detection:**  
  Automatically groups attendance records by employee and date for a chosen day, and identifies duplicate attendance groups.

- **Error Checking:**  
  Checks for inconsistent check-in and check-out times within duplicate groups. If inconsistencies are detected, the system notifies the user for manual intervention.

- **Preview Cleanup:**  
  Offers a detailed preview of which records will be retained and which will be removed before executing the cleanup.

- **Safe Cleanup Operation:**  
  Requires user confirmation before deleting duplicate records, ensuring no accidental data loss occurs.

- **User-Friendly Interface:**  
  An intuitive wizard view that displays notifications, error messages, and summaries of operations performed.

## Requirements

- **Odoo Version:** Odoo 17  
- **Dependencies:**  
  - The `hr_attendance` module must be installed.
  - Python 3.x

## Installation

1. **Clone or Download the Module:**

   ```bash
   git clone <your-repository-url>
   ```

2. **Place the Module:**

   Copy the module folder (e.g., `attendance_cleaner`) into your Odoo `addons` directory.

3. **Update the App List:**

   Restart the Odoo server and update the apps list from the Odoo interface:
   - Navigate to the Apps menu.
   - Click on "Update Apps List."

4. **Install the Module:**

   Locate "Attendance Cleaner" in the apps list and install it.

## Usage

1. **Access the Wizard:**

   Navigate to the Attendance Cleanup Wizard from the appropriate menu (e.g., under HR or a dedicated module menu).

2. **Operate the Wizard:**

   - **Select Date:**  
     Choose the date for which you wish to check and clean up attendance records.
   - **Check Errors:**  
     Click the **Check Errors** button to display any duplicate attendance groups for the selected date.
   - **Preview Cleanup:**  
     Click **Preview Cleanup** to see a detailed summary of records that will be retained and removed.
   - **Confirm Cleanup:**  
     Tick the confirmation checkbox and click **Clean Records** to execute the cleanup.

3. **Review Notifications:**

   The system will display notifications for error messages, cleanup previews, or successful operations.

## Security

Ensure the `ir.model.access.csv` file is correctly configured. For example:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_attendance_cleanup_wizard,access_attendance_cleanup_wizard,model_attendance_cleanup_wizard,,1,1,1,1
access_hr_attendance,access_hr_attendance,hr_attendance.model_hr_attendance,,1,1,1,1
```

This grants the necessary access rights for the wizard and HR attendance models. Also, include the proper dependencies in your module's manifest (e.g., `"hr_attendance"`).

## Developer Notes

- The wizard groups attendance records by employee and date.
- The cleanup logic preserves the first and last records while deleting intermediate duplicates.
- Inconsistent check-in/check-out times trigger a warning, prompting manual resolution.
- Logging is integrated for debugging and audit trails.

## License

Specify the license under which this module is distributed (e.g., AGPL-3).

## Contact

For support or contributions, please contact:  
**Sabry Youssef 01000059085 egypt**  
[Link to Repository](<your-repository-url>)

---

This README provides a comprehensive overview of the module, from installation and usage to development notes and security configuration. Adjust the content as needed for your specific project details.