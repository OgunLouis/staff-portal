import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staff_portal.settings")  # Replace with your actual project name
django.setup()

from accounts.models import CustomUser

# Update all users with NULL phone number to an empty string
CustomUser.objects.filter(phone_number__isnull=True).update(phone_number="")

print("✅ NULL phone numbers fixed!")
