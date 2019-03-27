from time import time
from datetime import timedelta

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=150, db_index=True)
    slug = models.SlugField('Наименование в адресной строке',
                            max_length=150, blank=True, unique=True)
    body = models.TextField('Содержание', blank=True, db_index=True)
    tags = models.ManyToManyField(
        'Tag', blank=True, related_name='posts', verbose_name='Тэги')
    pub_date = models.DateTimeField('Дата публикации', blank=True)

    # методы для переадресации:
    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    # переопределение метода сохранения поста с учётом пустого слага:
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        if not self.pub_date:
            self.pub_date = timezone.now()
        super().save(*args, **kwargs)

    # вспомогательные методы строкового представления и определения даты публикации:
    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    # упорядочивание постов по дате публикации от самого нового к более старым:
    class Meta:
        ordering = ['-pub_date']


class Tag(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    slug = models.SlugField(
        'Наименование в адресной строке', blank=True, unique=True)

    # методы для переадресации:
    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    # переопределение метода сохранения тэга с учётом пустого слага:
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    # строковое представление тэга:
    def __str__(self):
        return self.title

    # упорядочивание тэгов по названию в алфавитном порядке:
    class Meta:
        ordering = ['title']
