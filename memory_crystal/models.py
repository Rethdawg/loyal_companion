from django.db import models
from tinymce.models import HTMLField
import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages

# Create your models here.


class Memo(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Last modified')
    slug = models.SlugField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = HTMLField()
    STATUS = (
        ('D', 'Draft'),
        ('P', 'Published'),
        ('A', 'Archived')
    )
    status = models.CharField(choices=STATUS, default=0, max_length=1, verbose_name='Status')
    category = models.ManyToManyField('Category', related_name='memos', help_text='Memo categories', blank=True)

    class Meta:
        ordering = ['last_modified', 'pub_date']

    @property
    def all_categories(self):
        return ', '.join(cat.name for cat in self.category.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title)
            else:
                self.slug = slugify(self.content[:20])
        super(Memo, self).save(*args, **kwargs)

    def __str__(self):
        if self.title:
            return f'{self.title}; Published: {self.pub_date}'
        else:
            return f'{self.content[:30]}; Published: {self.pub_date}'


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    memo = models.ManyToManyField(Memo, related_name='categories', blank=True)

    def __str__(self):
        return f'{self.name.title()}'


class Birthday(models.Model):
    person = models.CharField(max_length=100, unique=True, help_text='Birthday person')
    bdate = models.DateField(help_text='YYYY-MM-DD', verbose_name='Date')

    def renew_birthday(self):
        if self.bdate < datetime.date.today():
            next_year = datetime.date.today().year + 1
            self.bdate = self.bdate.replace(year=next_year)
            self.save()

    def alert_user(self, request):
        remaining_days = timezone.now().date() - self.bdate
        if datetime.timedelta(days=15) <= remaining_days <= datetime.timedelta(days=28):
            messages.info(request, f'{self.person}\'s birthday is coming up soon!')
        elif (datetime.timedelta(days=2) <= remaining_days <= datetime.timedelta(days=14) or
              (datetime.timedelta(days=2) <= remaining_days <= datetime.timedelta(days=7))):
            messages.info(request, f'{self.person}\'s birthday is coming up on the {self.bdate.day}!!')
        elif remaining_days == datetime.timedelta(days=1):
            messages.warning(request, f'{self.person}\'s birthday is tomorrow!')
        elif remaining_days == datetime.timedelta(days=0):
            messages.error(request, f'!!!{self.person}\'s birthday is today!!!')

    def __str__(self):
        return f'{self.person}, {self.bdate}'


class BirthdayNote(models.Model):
    birthday = models.ForeignKey(to=Birthday, on_delete=models.CASCADE, help_text='Associated birthday',
                                 related_name='notes')
    pub_date = models.DateTimeField(auto_now_add=True, help_text='Date created')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = HTMLField()

    def __str__(self):
        if self.title:
            return f'Note: {self.title} for {self.birthday.person}; Pub: {self.pub_date}'
        else:
            return f'Note: {self.content[:30]} for {self.birthday.person}; Pub: {self.pub_date}'
