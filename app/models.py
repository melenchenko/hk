from django.conf import settings
from django.db import models
from django.utils import timezone

class Load(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=40, default='Demo')

    def __str__(self):
        return self.title


class Region(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Settings(models.Model):
    module = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return self.module + '.' + self.key + '=' + self.value


class Family(models.Model):
    pass


class Person(models.Model):
    fullname = models.CharField(max_length=200)
    birthday = models.DateField(blank=True)
    deathday = models.DateField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    mother = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    #father = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='father')
    city = models.ForeignKey(Family, on_delete=models.CASCADE)
    month_income = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    gender = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.fullname


class SpecialAccountType(models.Model):
    name = models.CharField(max_length=500)


class SpecialAccount(models.Model):
    data = models.TextField(blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.ForeignKey(SpecialAccountType, on_delete=models.CASCADE)


class PaymentType(models.Model):
    name = models.CharField(max_length=500)
    fixed_sum = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    is_regular = models.BooleanField(default=False)
    period = models.CharField(max_length=20, blank=True)
    natural = models.BooleanField(default=False)
    special_account_type = models.ForeignKey(SpecialAccountType, on_delete=models.CASCADE, blank=True, default='')


class PayerType(models.Model):
    name = models.CharField(max_length=500)


class Payer(models.Model):
    payer_type = models.ForeignKey(PayerType, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)


class Payment(models.Model):
    payment_sum = models.DecimalField(max_digits=20, decimal_places=2)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    payment_date = models.DateField()
    for_whom = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, related_name='for_whom')