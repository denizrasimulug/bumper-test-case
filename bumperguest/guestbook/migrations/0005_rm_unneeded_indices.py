# Generated by Django 5.1.2 on 2024-11-01 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guestbook', '0004_change_entry_created_date_field_name'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='entry',
            name='guestbook_e_guest_i_295b5c_idx',
        ),
        migrations.RemoveIndex(
            model_name='entry',
            name='guestbook_e_ulid_70adef_idx',
        ),
    ]
