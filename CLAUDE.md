# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern web application that displays working location schedules for team members. The application fetches data from a JSON file and renders it as responsive cards with color-coded location badges.

## Architecture

- `index.html`: Modern single-page web application with responsive design
- `export_working_locations.py`: Python script that fetches working location data from Google Calendar
- `people.json`: Data source containing working location schedules (auto-generated)
- `update-working-locations.sh`: Shell script that updates and commits `people.json`
- `requirements.txt`: Python dependencies for Google Calendar API integration
- `credentials.json`: Google OAuth credentials (not tracked in git)
- `token.json`: OAuth refresh token (not tracked in git)

## Data Flow

1. `export_working_locations.py` authenticates with Google Calendar API
2. The script fetches working location events from all accessible calendars
3. Data is formatted and written to `people.json`
4. `update-working-locations.sh` runs the Python script and commits changes
5. The web application fetches data from GitHub raw URL and displays it

## Key Commands

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Update working locations data
```bash
./update-working-locations.sh
```

### Test Python script directly
```bash
python3 export_working_locations.py
```

### Serve the web application locally
```bash
python3 -m http.server 8000
```

## Important Notes

- The application expects `people.json` to have a structure with a `people` array
- Each person has `name` and `days` properties  
- The `days` array contains objects with `timestamp` and `location` properties
- Location badges are color-coded: green (office), orange (home), purple (remote), blue (default)
- First-time setup requires Google Calendar API authentication via browser
- The web interface is fully responsive and works on mobile devices