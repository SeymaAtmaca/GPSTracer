# Generated by Django 5.0.7 on 2024-09-08 08:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracer', '0003_friendrequest_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='is_accepted',
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=255),
        ),
    ]
