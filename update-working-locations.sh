# Update the working locations
python3 /Users/roelvangils/Repositories/google-cal-working-locations/export-working-locations-gcal.py >people.json

# If 'people.json' has been changed, we stage and commit it
if git status --porcelain | grep -q "M people.json"; then
    git add people.json
    git commit -m "people.json has been updated."
    git push --set-upstream origin master
    echo "Updated."
else
    echo "No changes."
fi
