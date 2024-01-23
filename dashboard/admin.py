from django.contrib import admin
from .models import FeedEntry
# Register your models here.


class FeedEntryAdmin(admin.ModelAdmin):
    model = FeedEntry
    list_display = ('entry_type', 'title', 'description', 'pub_date')


admin.register(FeedEntry, FeedEntryAdmin)
