from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Finance_site.Type.NON)


class Finance_site(models.Model):

    class Type(models.TextChoices):
        INCOME = 'Доход'
        EXPENSES = 'Расход'
        NON = 'Не выбрано'

    operation_type = models.CharField(max_length=10, choices=Type.choices, default=Type.NON, verbose_name='Тип операции')
    operation_name = models.CharField(max_length=255, verbose_name='Название операции')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    amount = models.IntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='posts', verbose_name='Автор')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    # time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    # Снимем из комментов, если сделаем такую функцию
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.operation_name

    class Meta:
        verbose_name = 'Операции'
        verbose_name_plural = "Операции"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория операции')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})