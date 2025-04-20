import os
import django

# Set environment variable to point to your Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JSKLegalInsights.settings")

# Setup Django
django.setup()

# Now do the dumpdata
from django.core.management import call_command

with open("backup.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", indent=2, stdout=f)
