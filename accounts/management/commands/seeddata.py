from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from tasks.models import Task, Offer, Review
from faker import Faker
import random
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed 15 users with detailed profiles and realistic tasks.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Reset data
        Review.objects.all().delete()
        Offer.objects.all().delete()
        Task.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("🚨 All existing data wiped.")

        # Australian postcodes
        aus_postcodes = ["2000", "2031", "2150", "3000", "3121", "4000", "4217", "5000", "6000", "7010"]

        # Task title examples
        task_titles = [
            "Clean the backyard",
            "Assemble IKEA furniture",
            "Fix leaking tap",
            "Set up home Wi-Fi",
            "Wash car inside and out",
            "Help move furniture",
            "Paint a small room",
            "Install curtain rods",
            "Tidy up garden bed",
            "Clean windows and screens"
        ]

        # Skill examples
        skill_sets = [
            "Gardening, Mowing, Pruning",
            "Furniture Assembly, Carpentry",
            "Plumbing, Maintenance",
            "Tech Setup, Troubleshooting",
            "Window Cleaning, General Cleaning",
            "Delivery, Driving, Logistics"
        ]

        # Task categories
        categories = ['Cleaning', 'Gardening', 'Delivery', 'Repairs', 'IT Help']

        for _ in range(15):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "password123"

            user = User.objects.create_user(username=username, email=email, password=password)

            Profile.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                postcode=random.choice(aus_postcodes),
                bio=fake.sentence(nb_words=12),
                skills=random.choice(skill_sets),
                role=random.choice(['get', 'earn']),
                account_type=random.choice(['individual', 'business'])
            )

            Task.objects.create(
                title=random.choice(task_titles),
                description=fake.paragraph(nb_sentences=2),
                location=fake.city(),
                budget=Decimal(random.randint(80, 300)),
                due_type=random.choice(['on_date', 'before_date', 'flexible']),
                due_date=now().date() + timedelta(days=random.randint(3, 14)),
                posted_by=user,
                category=random.choice(categories)
            )

        self.stdout.write(self.style.SUCCESS("✅ 15 users with realistic profiles and tasks created."))
