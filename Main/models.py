from django.contrib.auth.models import User
from django.db.models import JSONField
from django.db import models


class Separator(models.Model):
    separator = models.CharField(max_length=1, verbose_name='Разделитель')
    description = models.CharField(max_length=32, verbose_name='Описание')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Разделитель'
        verbose_name_plural = 'Разделители'


class StringCharacter(models.Model):
    character = models.CharField(max_length=1, verbose_name='Символ')
    description = models.CharField(max_length=32, verbose_name='Описание')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Строковый символ'
        verbose_name_plural = 'Строковые символы'


class Schema(models.Model):
    name = models.CharField(max_length=32, verbose_name='Имя', null=True)
    modified_time = models.DateField(verbose_name="Дата изменения", null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', null=True)
    separator = models.ForeignKey(Separator, on_delete=models.CASCADE, null=True)
    string_character = models.ForeignKey(StringCharacter, on_delete=models.CASCADE, null=True)

    @property
    def columns(self):
        return Column.objects.filter(schema=self).order_by('order')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'


class ColumnType(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    specials = JSONField(null=True, verbose_name='Дополнительные параметры')
    validator = models.CharField(null=True, max_length=32, verbose_name='Класс-валидатор')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип колонки'
        verbose_name_plural = 'Типы колонок'


class Column(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, verbose_name='Таблица')
    col_type = models.ForeignKey(ColumnType, on_delete=models.CASCADE, verbose_name='Тип колонки')
    name = models.CharField(verbose_name='Имя колонки', max_length=32)
    order = models.IntegerField(verbose_name='Порядковый номер')
    extras = JSONField(verbose_name='Дополнительные параметры', null=True)

    def __str__(self):
        return self.schema.name + ' | ' + self.name

    class Meta:
        verbose_name = 'Колонка'
        verbose_name_plural = 'Колонки'


class DataSet(models.Model):
    statuses = [
        ('P', 'Processing'),
        ('R', 'Ready'),
        ('I', 'In queue'),
        ('F', 'Failed')
    ]
    schema = models.ForeignKey(Schema, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=2, choices=statuses, null=True)
    created = models.DateField()
    data = JSONField(verbose_name='Данные', null=True)

    def __str__(self):
        return f'{self.schema} ({self.id})'

    class Meta:
        verbose_name = 'Датасет'
        verbose_name_plural = 'Датасеты'
