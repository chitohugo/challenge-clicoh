import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from api.services import PriceDollar
from challenge import settings

price_dollar = PriceDollar.get_price()


class DataAwareModel(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False
                          )

    def __str__(self):
        return str(self.id)


class Product(DataAwareModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='products'
                             )
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Order(DataAwareModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orders'
                             )

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = 0
        order_details = OrderDetail.objects.all().filter(order=str(self.id))
        for item in order_details:
            total += item.product.price
        return f'{total:.2f}'

    @property
    def get_total_usd(self):
        total = float(self.get_total) / price_dollar
        return f'{total:.2f}'


class OrderDetail(DataAwareModel):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='order_details'
                              )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='order_details'
                                )

    def __str__(self):
        return str(self.id)
