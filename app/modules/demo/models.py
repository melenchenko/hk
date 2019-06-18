from django.db import models
from app.models import Load
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv

@receiver(post_save, sender=Load)
def demo_saver(sender, instance, **kwargs):
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
