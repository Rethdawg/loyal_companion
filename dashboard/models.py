from django.db import models
# Create your models here.


class FeedEntry(models.Model):
    """
    Class used by entries in the app's feeds.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField(blank=True, null=True)
    entry_type = models.CharField(max_length=200)
    guid = models.CharField(max_length=200)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.entry_type}: {self.title}'


class SteamGameFeed(models.Model):
    """
    Class that describes a steam game of interest for parsing.
    """
    title = models.CharField(max_length=200)
    appid = models.IntegerField(verbose_name='App ID')

    @property
    def rss_link(self) -> str:
        """
        Generates an rss feed link from the app id.
        :return: URL as a string
        """
        return f'https://store.steampowered.com/feeds/news/app/{self.appid}/'

    def __str__(self):
        return self.title


class WebsiteFeed(models.Model):
    """
    Class that describes a website of interest for parsing.
    """
    title = models.CharField(max_length=200)
    rss_link = models.URLField()

    def __str__(self):
        return self.title


class CitiesForWeather(models.Model):
    city_country = models.CharField(max_length=100, verbose_name='City')

    def __str__(self):
        return self.city_country
