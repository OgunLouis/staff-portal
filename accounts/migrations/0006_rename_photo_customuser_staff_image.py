# Generated by Django 5.1.1 on 2025-07-23 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_next_of_kin_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='photo',
            new_name='staff_image',
        ),
    ]
