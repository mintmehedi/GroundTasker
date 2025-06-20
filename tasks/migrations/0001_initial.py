# Generated by Django 4.2.21 on 2025-05-25 19:11

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('due_type', models.CharField(choices=[('on_date', 'On date'), ('before_date', 'Before date'), ('flexible', "I'm flexible")], max_length=20)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('bookmarked_by', models.ManyToManyField(blank=True, related_name='bookmarked_tasks', to=settings.AUTH_USER_MODEL)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(blank=True, max_length=15, null=True)),
                ('feedback', models.TextField(blank=True, max_length=2000, null=True)),
                ('reviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewee', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='tasks.task')),
            ],
        ),
    ]
