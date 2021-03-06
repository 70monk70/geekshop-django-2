# Generated by Django 3.2.8 on 2021-11-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'Формируется'), ('STP', 'Отправлен в обработку'), ('PD', 'Оплачен'), ('PRD', 'Обрабатывается'), ('RDY', 'Готов к выдаче'), ('CNC', 'Отменен')], default='FM', max_length=3, verbose_name='статус'),
        ),
    ]
