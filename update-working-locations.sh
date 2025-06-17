#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Update the working locations
python3 "$SCRIPT_DIR/export_working_locations.py" > "$SCRIPT_DIR/people.json"

# Check if the command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to export working locations"
    exit 1
fi

# If 'people.json' has been changed, we stage and commit it
cd "$SCRIPT_DIR"
if git status --porcelain | grep -q "M  people.json"; then
    git add people.json
    git commit -m "people.json has been updated."
    git push --set-upstream origin master
    echo "Updated and pushed to repository."
else
    echo "No changes detected."
fi