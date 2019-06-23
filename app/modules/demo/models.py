from django.db import models
from app.models import Load, Payment, Person, Payer, PaymentType, City, IncomeType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
import csv
import datetime, math


DEMO_SCHEMA = {
    'moduleName': 'Demo',
    'modelName': 'gauss',
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


DEMO_SCHEMA_priz3 = {
    'moduleName': 'DEMO_SCHEMA_priz3',
    'modelName': 'knn',
    'fields': {
        'target': '_priz3',
        'vars': ('_cap_count',
                 'birthday',
                 'month_income', 'city_id', 'gender', 'work_status', "main_income_type_id", "child_count", "_sum", "_cnt"),
        'decorators': {
            'birthday': lambda d, skip_id = False: math.floor((datetime.date.today() - d).days/365.2425),
            'city_id': lambda c, skip_id = False: c if skip_id else getattr(c, 'id'),
        }
    }
}


# @receiver(post_save, sender=Load)
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


class PredictBDForm(forms.Form):
    pass


class Priz3Form(forms.Form):
    _cap_count = forms.FloatField(min_value=0)
    birthday = forms.DateField()
    month_income = forms.FloatField(min_value=0)
    city_id = forms.ModelChoiceField(City.objects.all())
    gender = forms.IntegerField(min_value=0, max_value=1)
    work_status = forms.IntegerField(min_value=0, max_value=3)
    main_income_type_id = forms.ModelChoiceField(IncomeType.objects.all())
    child_count = forms.IntegerField(min_value=0, max_value=10)
    _sum = forms.FloatField(min_value=0)
    _cnt = forms.IntegerField(min_value=0)


class SettingsForm(forms.Form):
    load_id = forms.ModelChoiceField(queryset=Load.objects.filter(type='Demo'))


BIGDATA_CONFIG = {
    'priz3': {
        'form': Priz3Form,
        'schema': DEMO_SCHEMA_priz3,
    }
}
