from django.db import models
from tinymce.models import HTMLField
import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages

# Create your models here.


class Memo(models.Model):
    """
    Class that describes a memo model.
    """
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Last modified')
    slug = models.SlugField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    content = HTMLField()
    category = models.ManyToManyField('Category', related_name='memos', help_text='Memo categories', blank=True)

    class Meta:
        ordering = ['last_modified', 'pub_date']

    @property
    def all_categories(self) -> str:
        """
        Joins categories into a string.
        :return: str
        """
        return ', '.join(cat.name for cat in self.category.all())

    def save(self, *args, **kwargs):
        """
        Modified save to slugify the title of the memo.
        :param args: args
        :param kwargs: kwargs
        :return: None
        """
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title[:10] + str(self.id))
        super(Memo, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """
        String name definition for class for easier readability.
        :return: str
        """
        return f'{self.title}; Published: {self.pub_date}'


class Category(models.Model):
    """
    Class that describes a category model.
    """
    name = models.CharField(max_length=200, unique=True)
    memo = models.ManyToManyField(Memo, related_name='categories', blank=True)

    def __str__(self) -> str:
        """
        String name definition for class for easier readability.
        :return: str
        """
        return f'{self.name.title()}'

    class Meta:
        verbose_name_plural = 'Categories'


class Birthday(models.Model):
    """
    Class that describes a birthday model.
    """
    person = models.CharField(max_length=100, unique=True)
    bdate = models.DateField(help_text='YYYY-MM-DD', verbose_name='Date')

    def renew_birthday(self):
        """
        Increments the bdate attribute of a Birthday instance by one year from the current Django server year.
        :return: None
        """
        if self.bdate < datetime.date.today():
            next_year = datetime.date.today().year + 1
            self.bdate = self.bdate.replace(year=next_year)
            self.save()

    @property
    def soon(self) -> str | bool:
        """
        Function that determines how close the Birthday instance is to the current date, and returns either a string
        to modify the style of a text, or a False value if the instance is not close enough to Django server's current
        date.
        :return: str or bool
        """
        remaining_days = self.bdate - timezone.now().date()
        if timezone.timedelta(days=-1) <= remaining_days <= timezone.timedelta(days=1):
            return 'danger'
        elif timezone.timedelta(days=-1) <= remaining_days <= timezone.timedelta(days=14):
            return 'warning'
        elif timezone.timedelta(days=-1) <= remaining_days <= timezone.timedelta(days=30):
            return 'info'
        else:
            return False

    @property
    def passed(self) -> bool:
        """
        Checks if the Birthday instance's bdate attribute is behind today's date. Returns True if it is, False if it is
        not.
        :return: bool
        """
        remaining_days = timezone.now().date() - self.bdate
        if remaining_days < timezone.timedelta(-1):
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        String name definition for class for easier readability.
        :return: str
        """
        return f'{self.person}, {self.bdate}'


class BirthdayNote(models.Model):
    """
    Class that describes a birthday note model.
    """
    birthday = models.ForeignKey(to=Birthday, on_delete=models.CASCADE, help_text='Associated birthday',
                                 related_name='notes')
    pub_date = models.DateTimeField(auto_now_add=True, help_text='Date created')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = HTMLField()

    def __str__(self) -> str:
        """
        String name definition for class for easier readability.
        :return: str
        """
        if self.title:
            return f'Note: {self.title} for {self.birthday.person}; Pub: {self.pub_date}'
        else:
            return f'Note: {self.content[:10]} for {self.birthday.person}; Pub: {self.pub_date}'
