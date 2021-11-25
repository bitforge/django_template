from django.contrib.admin import site

from {{ project_name }} import models
from admin import admins;

# Register {{ project_name }} admins
site.register(models.Entry, admins.EntryAdmin)
