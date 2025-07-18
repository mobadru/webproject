# Generated by Django 5.2.3 on 2025-06-23 22:48

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_tenant_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(default=datetime.date(2025, 12, 1)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_date',
            field=models.DateField(default=datetime.date(2025, 1, 1)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='myapp.tenant'),
        ),
    ]
