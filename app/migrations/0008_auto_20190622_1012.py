# Generated by Django 2.2.1 on 2019-06-22 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190621_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='family',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='app.Family'),
        ),
        migrations.AddField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='_father', to='app.Person'),
        ),
        migrations.AddField(
            model_name='person',
            name='health_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='for_whom',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='_for_whom', to='app.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.City'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='_mother', to='app.Person'),
        ),
    ]
