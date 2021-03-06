# Generated by Django 3.2.8 on 2021-11-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'Формируется'), ('STP', 'Отправлен в обработку'), ('PD', 'Оплачен'), ('PRD', 'Обрабатывается'), ('RDY', 'Готов к выдаче'), ('CMP', 'Завершен'), ('CNC', 'Отменен')], default='FM', max_length=3, verbose_name='статус'),
        ),
    ]
