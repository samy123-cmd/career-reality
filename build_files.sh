# Build script
echo "Building the project..."
pip install -r requirements.txt

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

echo "Build End"
