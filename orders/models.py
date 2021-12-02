from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product


# Create your models here.


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'
    COMPLETE = 'CMP'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PAID, 'Оплачен'),
        (PROCEEDED, 'Обрабатывается'),
        (READY, 'Готов к выдаче'),
        (COMPLETE, 'Завершен'),
        (CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)

    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ № {self.id}: для пользователя {self.user.username}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return items.count()

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.status = 'CNC'
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


# class OrderItemQuerySet(models.QuerySet):
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += self.quantity
#             object.product.save()
#         super(OrderItemQuerySet, self).delete()


class OrderItem(models.Model):
    # objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(
        Order,
        related_name='orderitems',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    def get_product_cost(self):
        return self.product.price * self.quantity
