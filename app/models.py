from django.conf import settings
from django.db import models
from django.utils import timezone

class Load(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=40, default='Demo')

    def __str__(self):
        return self.title

class Demo(models.Model):
    IRISES = (
        (0, 'Iris-setosa'),
        (1, 'Iris-versicolor'),
        (2, 'Iris-virginica'),
    )
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    iris = models.IntegerField(choices=IRISES)
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()

    def __str__(self):
        return self.iris
