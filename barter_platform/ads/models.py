from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('toys', 'Игрушки'),
        ('electronics', 'Электроника'),
        ('sports', 'Товары для спорта'),
        ('home', 'Товары для дома'),
        ('books', 'Книги и журналы'),
        ('clothes', 'Одежда'),
        ('other', 'Другое')
    ]

    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=None,
                             verbose_name='Пользователь')

    title = models.CharField(max_length=100,
                             verbose_name='Название')

    description = models.TextField(max_length=1000,
                                   verbose_name='Описание')

    image_url = models.ImageField(upload_to="images/",
                                blank=True,
                                null=True,
                                verbose_name='Фото')

    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES,
                                verbose_name='Категория')

    condition = models.CharField(max_length=10,
                                 choices=CONDITION_CHOICES,
                                 verbose_name='Состояние')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=None,
                             verbose_name='Пользователь')
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE,
                                  verbose_name='Предлагаемая вещь',
                                  related_name='sent_proposals',
                                  default=None)

    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE,
                                    verbose_name='Желаемая вещь',
                                    related_name='received_proposals',
                                    default=None)
    comment = models.CharField(max_length=200,
                               verbose_name='Комментарий')

    choices = [
        ('W', 'Ожидает'),
        ('Y', 'Принято'),
        ('N', 'Отклонено'),
    ]
    status = models.CharField(choices=choices, default='Ожидает',
                              verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
