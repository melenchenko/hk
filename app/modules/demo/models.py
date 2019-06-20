from django.db import models
from app.models import Load
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
import csv

DEMO_SCHEMA = {
    'moduleName': 'Demo',
    'fields': {
        'target': 'iris',
        'vars': ('sepal_length', 'sepal_width', 'petal_length', 'petal_width'),
    },
    'targets': {
        'Iris-setosa': {
            'color': 'rgba(255, 182, 193, .9)'
        },
        'Iris-versicolor': {
            'color': 'rgba(3, 212, 3, .9)'
        },
        'Iris-virginica': {
            'color': 'rgba(46, 82, 193, .9)'
        },
    },
    'x': 'sepal_length',
    'y': 'sepal_width',
}


@receiver(post_save, sender=Load)
def demo_saver(sender, instance, **kwargs):
    if instance.type == 'Demo':
        with open(instance.file.name, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                Demo.objects.create(
                    load=instance,
                    iris=row[4],
                    sepal_length=row[0],
                    sepal_width=row[1],
                    petal_length=row[2],
                    petal_width=row[3]
                )


class Demo(models.Model):
    IRISES = (
        ('Iris-setosa', 'Iris-setosa'),
        ('Iris-versicolor', 'Iris-versicolor'),
        ('Iris-virginica', 'Iris-virginica'),
    )
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    iris = models.CharField(max_length=40, choices=IRISES)
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()

    def __str__(self):
        return self.iris


class PredictForm(forms.ModelForm):
    class Meta:
        model = Demo
        fields = DEMO_SCHEMA['fields']['vars']

class SettingsForm(forms.Form):
    load_id = forms.ModelChoiceField(queryset=Load.objects.filter(type='Demo'))
