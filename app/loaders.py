from app.models import Load, Payment, Person, Payer, PaymentType
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv


# @receiver(post_save, sender=Load)
# def payment_saver(sender, instance, **kwargs):
def payment_saver(instance, **kwargs):
    if instance.type == 'Payment':
        with open(instance.file.name, newline='') as f:
            reader = csv.reader(f, delimiter=';', quotechar="'")
            for row in reader:
                success = True
                errors = []
                try:
                    person_ = Person.objects.get(snils=row[2])
                except:
                    success = False
                    errors.append('SNILS not found')
                try:
                    payer_ = Payer.objects.get(id=row[3])
                except:
                    success = False
                    errors.append('Payer ID not found')
                try:
                    payment_type_ = PaymentType.objects.get(id=row[4])
                except:
                    success = False
                    errors.append('Payment type ID not found')
                if success:
                    Payment.objects.create(
                        payment_date = row[0],
                        payment_sum = row[1],
                        person = person_,
                        payer = payer_,
                        payment_type = payment_type_
                    )
                return success, errors
