import django
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

django.setup()

try:
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin1234"
        )
        print("✅ Superuser created: admin / admin1234")
    else:
        print("Superuser already exists.")
except OperationalError:
    print("⚠️ Database not ready, skipping superuser creation.")
