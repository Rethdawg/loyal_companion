from django.core.management import BaseCommand
from dashboard.models import FeedEntry
# Command file for clearing all RSS feed entries from the database


def clear_feed_entries() -> None:
    """
    Function that clears all entries from the FeedEntry table. Used for testing and presentation purposes only.
    :return: None
    """
    for entry in FeedEntry.objects.all():
        entry.delete()


class Command(BaseCommand):
    """
    Custom command class used for clearing the FeedEntries table.
    """
    def handle(self, *args, **options):
        clear_feed_entries()
