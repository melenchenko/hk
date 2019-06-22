from .models import Person, Payment, PaymentType
import datetime


AGES = [
    [0, 18],
    [18, 25],
    [25, 30],
    [30, 35],
    [35, 40],
    [40, 45],
    [45, 50],
    [50, 55],
    [55, 60],
    [60, 65],
    [65, 70],
    [70, 80],
    [80, 90],
    [90, 1000],
]
AGE_NUMBER = 'DATE_FORMAT(FROM_DAYS(TO_DAYS(now()) - TO_DAYS(birthday)), "%%Y")+0'


def person_count():
    result = []
    for age in AGES:
        age_query = AGE_NUMBER + '>= ' + str(age[0]) + ' AND ' + AGE_NUMBER + '< ' + str(age[1])
        query = 'SELECT app_person.* FROM app_person WHERE ' + age_query
        persons_all = Person.objects.raw(query)
        persons_all_count = [0, 0]
        for person in persons_all:
            persons_all_count[person.gender] += 1
        query = 'SELECT DISTINCT app_person.id, app_person.gender FROM app_person INNER JOIN app_payment ON (app_person.id=app_payment.person_id) WHERE ' + age_query
        persons_with_payments = Person.objects.raw(query)
        persons_with_payments_count = [0, 0]
        for person in persons_with_payments:
            persons_with_payments_count[person.gender] += 1
        result.append({
            'age': age,
            'all': persons_all_count,
            'with_payments': persons_with_payments_count,
            'percent': list(map(lambda a, b: str(round(100 * b / a)) + '%', persons_all_count, persons_with_payments_count))
        })
    return result


def payment_sum():
    result = []
    query = '''SELECT pt.id, SUM(p.payment_sum) as s, pt.name 
        FROM app_payment p 
        INNER JOIN app_paymenttype pt ON (p.payment_type_id = pt.id)
        GROUP BY pt.id'''
    payments = Payment.objects.raw(query)
    for payment in payments:
        result.append({'name': payment.name, 'sum': payment.s})
    return result
