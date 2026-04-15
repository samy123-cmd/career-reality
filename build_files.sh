# Build script
set -e
echo "Building the project..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collect Static..."
python manage.py collectstatic --noinput --clear

echo "Build End"
