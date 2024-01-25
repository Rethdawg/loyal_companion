from django.core.management.base import BaseCommand
from django.conf import settings
from dashboard.models import FeedEntry, SteamGameFeed, WebsiteFeed
from currency_mogul.models import Currency
from currency_mogul.api_utils import all_currencies
from memory_crystal.models import Birthday
import feedparser
from dateutil import parser
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


def refresh_currency_list():
    """
    Refreshes the Currency table in the DB by updating it from a currency list called from the Frankfurter API.
    :return: None
    """
    for key, value in all_currencies.items():
        if not Currency.objects.filter(name__icontains=value).exists():
            new_currency = Currency(name=value,
                                    code=key)
            new_currency.save()


def save_new_entry(feed: feedparser) -> None:
    """
    Parses the given RSS feed and saves it as an entry in the database.
    :param feed: feedparser object
    :return: None
    """
    entry_type = feed.channel.title

    for item in feed.entries:
        if not FeedEntry.objects.filter(guid=item.guid):
            entry = FeedEntry(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                # image=item.enclosure if item.enclosure else None,
                entry_type=entry_type,
                guid=item.guid
            )
            entry.save()


def fetch_steam_news() -> None:
    """
    Parses the rss feed of each SteamGameFeed object in the database.
    :return: None
    """
    for game in SteamGameFeed.objects.all():
        feed_obj = feedparser.parse(game.rss_link)
        save_new_entry(feed_obj)


def fetch_website_news():
    """
    Parses the rss feed of each WebsiteFeed object in the database.
    :return:
    """
    for website in WebsiteFeed.objects.all():
        feed_obj = feedparser.parse(website.rss_link)
        save_new_entry(feed_obj)


def delete_old_entries(max_age=604_800):
    """
    Deletes execution log entries older than max_age.
    :param max_age: int, default 604800
    :return: None
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def check_and_renew_birthdays() -> None:
    """
    Increment a Birthday instance bdate field by a year that returns True on its passed property.
    :return: None
    """
    for birthday in Birthday.objects.all():
        if birthday.passed:
            birthday.renew_birthday()


class Command(BaseCommand):
    """
    Custom command class used for setting up apscheduler jobs.
    """
    def handle(self, *args, **options):
        fetch_steam_news()
        fetch_website_news()
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            fetch_steam_news,
            trigger='interval',
            minutes=30,
            id='Steam News',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job: Steam News')

        scheduler.add_job(
            fetch_website_news,
            trigger='interval',
            minutes=30,
            id='Website News',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job: Website News')

        scheduler.add_job(
            delete_old_entries,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='Delete Old News',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job: Delete Old News')

        scheduler.add_job(
            refresh_currency_list,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='Refresh currencies',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job: Refresh currencies')

        scheduler.add_job(
            check_and_renew_birthdays,
            trigger=CronTrigger(
                hour=0, minute=0, second=1
            ),
            id='Check and increment birthdays',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job: Check and increment birthdays')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully.')
