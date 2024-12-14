from django.db import models


class Finance_site(models.Model):

    class Type(models.TextChoices):
        INCOME = '0', 'Доход'
        EXPENSES = '1', 'Расход'

    operation_type = models.CharField(max_length=10, choices=Type.choices, default=1, verbose_name='Тип операции')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории', null=True)
    operation_name = models.CharField(max_length=255, verbose_name='Название операции')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    amount = models.IntegerField(verbose_name='Сумма')
    author = models.ForeignKey('auth.user', on_delete=models.PROTECT, verbose_name='Автор', editable=False)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    objects = models.Manager()

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
    type = models.BooleanField(verbose_name='Тип операции', default=1)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = "Операции"

    def __str__(self):
        return self.name
