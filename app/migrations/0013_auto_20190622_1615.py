# Generated by Django 2.2.1 on 2019-06-22 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20190622_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='fixed_sum',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
