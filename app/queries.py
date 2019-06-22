from .models import Person, Payment
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
        persons_all_count = len(list(persons_all))
        query = 'SELECT app_person.* FROM app_person INNER JOIN app_payment ON (app_person.id=app_payment.person_id) WHERE ' + age_query
        persons_with_payments = Person.objects.raw(query)
        persons_with_payments_count = len(list(persons_with_payments))
        result.append({
            'age': age,
            'all': persons_all_count,
            'with_payments': persons_with_payments_count,
            'percent': str(round(persons_with_payments_count / persons_all_count * 100)) + '%'
        })
    return result
