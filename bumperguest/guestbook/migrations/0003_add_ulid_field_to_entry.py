# Generated by Django 5.1.2 on 2024-11-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guestbook', '0002_create_indices'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='ulid',
            field=models.CharField(default='', max_length=26, unique=True),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='entry',
            index=models.Index(fields=['ulid'], name='guestbook_e_ulid_70adef_idx'),
        ),
    ]