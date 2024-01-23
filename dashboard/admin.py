from django.contrib import admin
from .models import FeedEntry, SteamGameFeed, WebsiteFeed
# Register your models here.


class FeedEntryAdmin(admin.ModelAdmin):
    """
    Class that customises FeedEntry display in the admin panel.
    """
    model = FeedEntry
    list_display = ('entry_type', 'title', 'description', 'pub_date')


class SteamGameFeedAdmin(admin.ModelAdmin):
    """
    Class that customises SteamGameFeed display in the admin panel.
    """
    model = SteamGameFeed
    list_display = ('title', 'appid', 'rss_link')


class WebsiteFeedAdmin(admin.ModelAdmin):
    """
    Class that customises WebsiteFeed display in the admin panel.
    """
    model = WebsiteFeed
    list_display = ('title', 'rss_link')


admin.site.register(FeedEntry, FeedEntryAdmin)
admin.site.register(SteamGameFeed, SteamGameFeedAdmin)
admin.site.register(WebsiteFeed, WebsiteFeedAdmin)
