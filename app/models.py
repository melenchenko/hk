from django.conf import settings
from django.db import models
from django.utils import timezone

class Load(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text='Название выборки')
    file = models.FileField(upload_to='uploads/', help_text='Файл CSV')
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=40, default='Demo')

    def __str__(self):
        return self.title


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    population = models.IntegerField(default=100000)
    type = models.PositiveSmallIntegerField(default=1) #1 - город, 2 - село

    def __str__(self):
        return self.name


class Settings(models.Model):
    module = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return self.module + '.' + self.key + '=' + self.value


class FamilyPriznak(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Family(models.Model):
    fpriznak = models.ForeignKey(FamilyPriznak, on_delete=models.CASCADE, blank=True, default=None, null=True)
    child_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.fpriznak.name



class Priznak(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '{0}'.format(self.name)


class IncomeType(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name


class Person(models.Model):
    fullname = models.CharField(max_length=200)
    birthday = models.DateField(blank=True)
    deathday = models.DateField(blank=True, null=True, default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    mother = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='_mother', default=None, null=True)
    father = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='_father', default=None, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, blank=True, default=None, null=True)
    month_income = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    gender = models.PositiveSmallIntegerField(default=0)
    health_status = models.IntegerField(default=0)
    work_status = models.IntegerField(default=0) #0 - безработный, 1 - работающий, 3 - пенсионер, 2 - школьник и т.д.
    snils = models.CharField(max_length=50, blank=True, default='')
    suprug = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='_suprug', default=None, null=True)
    main_income_type = models.ForeignKey(IncomeType, on_delete=models.CASCADE, blank=True, default=None, null=True)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname


class PersonPriznakLink(models.Model):
    priznak = models.ForeignKey(Priznak, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    start = models.DateField(null=True, default=None, blank=True)
    end = models.DateField(blank=True, null=True, default=None)

    class Meta:
        unique_together = ('person', 'priznak')

    def __str__(self):
        return self.person.fullname + ': ' + self.priznak.name


class Capital(models.Model):
    start = models.DateField(null=True, default=None, blank=True)
    end = models.DateField(blank=True, null=True, default=None)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class SpecialAccountType(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class SpecialAccount(models.Model):
    data = models.TextField(blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.ForeignKey(SpecialAccountType, on_delete=models.CASCADE)


class PayerType(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=500)
    fixed_sum = models.DecimalField(max_digits=20, decimal_places=2, blank=True, default=None, null=True)
    is_regular = models.BooleanField(default=False)
    period = models.CharField(max_length=20, blank=True)
    natural = models.BooleanField(default=False)
    special_account_type = models.ForeignKey(SpecialAccountType, on_delete=models.CASCADE, blank=True, default=None, null=True)
    priznak = models.ForeignKey(Priznak, on_delete=models.CASCADE, blank=True, default=None, null=True)
    payer_type = models.ForeignKey(PayerType, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return self.name


class Payer(models.Model):
    payer_type = models.ForeignKey(PayerType, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return "%s" % self.name


class Payment(models.Model):
    payment_sum = models.DecimalField(max_digits=20, decimal_places=2)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, blank=True, default=None, null=True)
    payment_date = models.DateField()
    for_whom = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='_for_whom')

    def __str__(self):
        return "%s: %s руб" % (self.payment_type, self.payment_sum)


class Oprosnik(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=200)
    oprosnik = models.ForeignKey(Oprosnik, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return self.text


class Answers(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, default=None, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, default=None, null=True)
    value = models.IntegerField(default = 0)

    class Meta:
        unique_together = ('person', 'question')

    def __str__(self):
        return str(self.value)
