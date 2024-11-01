from django.contrib import admin

from guestbook.models import Entry, Guest

# Register your models here.

admin.site.register(Guest)
admin.site.register(Entry)