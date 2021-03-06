# Generated by Django 2.2.1 on 2019-06-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20190622_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PaymentType'),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='fixed_sum',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=20, null=True),
        ),
    ]
