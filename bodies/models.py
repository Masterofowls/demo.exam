import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_receive_code():

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Product(models.Model):

    name        = models.CharField(max_length=256, verbose_name="Название ")
    price       = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Цена (р.)")
    description = models.TextField(blank=True, verbose_name="Описание ")
    sku         = models.CharField(max_length=50, unique=True, verbose_name="Артикул")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.sku})"


class PickupPoint(models.Model):
  
    address = models.CharField(max_length=400, verbose_name="Адрес")

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"

    def __str__(self):
        return self.address


class Order(models.Model):
   
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('delivered', 'Завершен'),
    ]
    
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    products     = models.ManyToManyField(Product, verbose_name="Товары в заказе")
    createdAt    = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания ")
    deliveryDate = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    receiveCode  = models.CharField(max_length=20, default=generate_receive_code, verbose_name="Код")
    pickupPoint  = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, verbose_name="Пункт выдачи")
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус ")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-createdAt']

    def __str__(self):
        user_name = self.user.get_full_name() or self.user.username
        return f"Заказ #{self.id} - {user_name}"
    
    def get_skus(self):
        return ', '.join([p.sku for p in self.products.all()])


class Profile(models.Model):

    ROLE_CHOICES = [
        ('unauthorized', 'Неавторизирован'),
        ('authorized', 'Авторизирован'),
        ('editor', 'Редактор'),
        ('admin', 'Админ'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='authorized', verbose_name="Роль")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_editor(self):
        return self.role in ['editor', 'admin']
    
    def is_authorized(self):
        return self.role in ['authorized', 'editor', 'admin']
    
    
    
