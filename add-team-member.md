# Adding New Team Members

## For Team Members

1. **Share your Google Calendar**
   - Open Google Calendar
   - Go to Settings (⚙️) → Settings
   - Find your calendar in the left sidebar
   - Click "Share with specific people or groups"
   - Add the admin's email address
   - Select "See all event details" permission
   - Click "Send"

2. **Add Working Location events**
   - In Google Calendar, enable working locations
   - Set your daily working location (Home, Office, etc.)

## For Administrators

1. **Accept calendar invitations**
   - Check your email for calendar sharing invitations
   - Accept each invitation

2. **Set calendar descriptions**
   - Go to Google Calendar
   - Find the shared calendar in your sidebar
   - Click the 3 dots menu → Settings
   - In the "Description" field, enter the person's full name
   - Save the settings

3. **Run the update script**
   ```bash
   ./update-working-locations.sh
   ```

The new team members will appear automatically in the application!

## Troubleshooting

- If a person doesn't appear, check if:
  - Their calendar is properly shared
  - The calendar has a description set
  - They have working location events set
  
- If showing email instead of name:
  - Make sure to set the calendar description
  - The script falls back to calendar summary if no description exists