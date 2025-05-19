# 1. Make sure you're in the project root and inside the virtual environment
cd /path/to/CSCI334
source venv/bin/activate  # or use your method if on Windows

# 2. Create the new app
python manage.py startapp appname   # Replace 'appname' with your desired name

# 3. Register the new app in settings.py
# Open csci334_platform/settings.py and add the app name to INSTALLED_APPS like this:

INSTALLED_APPS = [
    ...
    'appname',  #  Add your app here
]

# 4. Make initial migrations for the app
python manage.py makemigrations appname

# 5. Apply the migrations to the database
python manage.py migrate

# 6. (Optional) Create templates and static folders if needed
mkdir appname/templates
mkdir appname/static