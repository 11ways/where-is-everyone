#!/usr/bin/env python3
"""Export working locations from Google Calendar."""

import datetime
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()


def authenticate():
    """Handle Google Calendar API authentication."""
    creds = None
    token_path = SCRIPT_DIR / 'token.json'
    credentials_path = SCRIPT_DIR / 'credentials.json'
    
    # Load existing token if available
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"Error: credentials.json not found at {credentials_path}")
                print("Please follow the setup instructions to obtain credentials.json")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def fetch_working_locations(service, days_ahead=7):
    """Fetch working locations from all calendars."""
    try:
        # Get list of all calendars
        calendar_list = service.calendarList().list().execute()
        
        # Prepare data structure with timestamp
        people_data = {
            "people": [],
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        # Time range: from now to N days ahead
        time_min = datetime.datetime.now(datetime.timezone.utc)
        time_max = time_min + datetime.timedelta(days=days_ahead)
        
        # Convert to RFC3339 format
        time_min_str = time_min.isoformat().replace('+00:00', 'Z')
        time_max_str = time_max.isoformat().replace('+00:00', 'Z')
        
        # Process each calendar
        for calendar in calendar_list.get('items', []):
            # Skip group calendars
            if calendar['id'].endswith('@group.v.calendar.google.com'):
                continue
            
            # Get calendar name (prefer description, fallback to summary)
            calendar_name = calendar.get('description', calendar.get('summary', 'Unknown'))
            
            # Skip if no proper name
            if not calendar_name or calendar_name == 'Unknown':
                continue
            
            # Skip non-person calendars (descriptions that are too long or contain certain keywords)
            skip_keywords = ['calendar', 'room', 'meeting', 'anniversary', 'anniversaries', 'co-working', 'privé', 'private']
            if len(calendar_name) > 60 or any(keyword in calendar_name.lower() for keyword in skip_keywords):
                continue
            
            # Fetch working location events
            try:
                events_result = service.events().list(
                    calendarId=calendar['id'],
                    timeMin=time_min_str,
                    timeMax=time_max_str,
                    maxResults=366,
                    singleEvents=True,
                    eventTypes='workingLocation',
                    orderBy='startTime'
                ).execute()
                
                events = events_result.get('items', [])
                
                # Always create person entry, even if no events
                person = {
                    'name': calendar_name,
                    'days': []
                }
                
                # Add each working location event
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    person['days'].append({
                        'timestamp': start,
                        'location': event.get('summary', 'Unknown location')
                    })
                
                # Add person even if they have no working locations set
                people_data['people'].append(person)
                    
            except HttpError as error:
                print(f"Error fetching events for {calendar_name}: {error}", file=sys.stderr)
                continue
        
        return people_data
        
    except HttpError as error:
        print(f"An error occurred: {error}", file=sys.stderr)
        return {"people": []}


def main():
    """Main function to export working locations."""
    # Authenticate
    creds = authenticate()
    
    # Build the service
    service = build('calendar', 'v3', credentials=creds)
    
    # Fetch working locations
    data = fetch_working_locations(service)
    
    # Output as JSON
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()