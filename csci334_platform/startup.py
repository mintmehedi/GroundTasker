from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
import logging

def create_admin_user():
    try:
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin1234",
                email="admin@example.com",
                password="admin1234"
            )
            logging.info("✅ Superuser created: admin / admin1234")
        else:
            logging.info("Superuser already exists.")
    except OperationalError:
        logging.warning("⚠️ Database not ready yet — skipping superuser creation.")
