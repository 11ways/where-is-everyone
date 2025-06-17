# Where is Everyone?

A web application that displays team members' working locations fetched from Google Calendar.

## Features

- Fetches working location data from Google Calendar
- Modern, responsive web interface with card-based layout
- Color-coded location badges (Office, Home, Remote)
- Automatic data updates via shell script
- GitHub Pages compatible

## Setup

### Prerequisites

- Python 3.6+
- Google Calendar API access
- Git repository with GitHub Pages enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/11ways/where-is-everyone.git
cd where-is-everyone
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up Google Calendar API credentials:
   - Follow [Google's quickstart guide](https://developers.google.com/calendar/quickstart/python) to obtain `credentials.json`
   - Place `credentials.json` in the repository root

4. Authenticate with Google Calendar:
```bash
python3 export_working_locations.py
```
This will open a browser for authentication and create `token.json`.

## Usage

### Update Working Locations

Run the update script to fetch latest data:
```bash
./update-working-locations.sh
```

This script:
- Fetches working locations from Google Calendar
- Updates `people.json`
- Commits and pushes changes if data has changed

### View the Web Application

- **GitHub Pages**: Visit `https://[username].github.io/where-is-everyone`
- **Local development**: 
  ```bash
  python3 -m http.server 8000
  # Then visit http://localhost:8000
  ```

## Data Format

The `people.json` file contains:
```json
{
  "people": [
    {
      "name": "Person Name",
      "days": [
        {
          "timestamp": "2024-01-15T09:00:00Z",
          "location": "Office"
        }
      ]
    }
  ]
}
```

## Files

- `index.html` - Modern web interface
- `export_working_locations.py` - Python script to fetch data from Google Calendar
- `update-working-locations.sh` - Shell script to update and commit data
- `people.json` - Working location data (auto-generated)
- `requirements.txt` - Python dependencies
- `credentials.json` - Google API credentials (not tracked in git)
- `token.json` - OAuth token (not tracked in git)

## Security

The following files are excluded from version control:
- `token.json` - Contains OAuth tokens
- `credentials.json` - Contains API credentials

## Customization

Location badges are color-coded based on keywords:
- Green: "office"
- Orange: "home"  
- Purple: "remote"
- Blue: default for other locations

## License

This project is open source and available under the MIT License.