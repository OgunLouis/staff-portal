# Generated by Django 5.1.1 on 2025-07-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_address_alter_customuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='next_of_kin_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
