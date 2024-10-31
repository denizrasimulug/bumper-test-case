from django.contrib import admin

from bumperguest.guestbook.models import Entry, Guest

# Register your models here.

admin.site.register(Guest)
admin.site.register(Entry)