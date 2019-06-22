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
INCOMES = [
    [0, 0.01],
    [0.01, 10000],
    [10000, 15000],
    [15000, 20000],
    [20000, 25000],
    [25000, 30000],
    [30000, 35000],
    [35000, 40000],
    [40000, 50000],
    [50000, 60000],
    [60000, 80000],
    [80000, 100000],
    [100000, 150000],
    [150000, 200000],
    [200000, 300000],
    [300000, 2000000000]
]
AGE_NUMBER = 'DATE_FORMAT(FROM_DAYS(TO_DAYS(now()) - TO_DAYS(birthday)), "%%Y")+0'


def person_count(need_age = [], need_all = False):
    result = []
    for age in AGES:
        age_query = AGE_NUMBER + '>= ' + str(age[0]) + ' AND ' + AGE_NUMBER + '< ' + str(age[1])
        query = 'SELECT app_person.* FROM app_person WHERE ' + age_query
        persons_all = Person.objects.raw(query)
        persons_all_count = [0, 0]
        for person in persons_all:
            persons_all_count[person.gender] += 1
        query = 'SELECT DISTINCT app_person.* FROM app_person INNER JOIN app_payment ON (app_person.id=app_payment.person_id) WHERE ' + age_query
        persons_with_payments = Person.objects.raw(query)
        persons_with_payments_count = [0, 0]
        for person in persons_with_payments:
            persons_with_payments_count[person.gender] += 1
        percent = list(map(lambda a, b: str(round(100 * b / a)) + '%', persons_all_count, persons_with_payments_count))
        data = []
        if age == need_age:
            if need_all:
                data = persons_all
            else:
                data = persons_with_payments
        result.append({
            'data': data,
            'age': age,
            'all': persons_all_count,
            'with_payments': persons_with_payments_count,
            'percent': percent,
        })
    return result


def payment_sum(need_data = False):
    result = []
    query = '''SELECT pt.id, SUM(p.payment_sum) as s, pt.name 
        FROM app_payment p 
        INNER JOIN app_paymenttype pt ON (p.payment_type_id = pt.id)
        GROUP BY pt.id'''
    payments = Payment.objects.raw(query)
    for payment in payments:
        result.append({'name': payment.name, 'sum': payment.s})
    return result


def beneficiary_by_income(need_income = [], need_all = False):
    result = []
    for income in INCOMES:
        income_query = 'month_income >= ' + str(income[0]) + ' AND month_income < ' + str(income[1])
        query = 'SELECT app_person.* FROM app_person WHERE ' + income_query
        persons_all = Person.objects.raw(query)
        persons_all_count = [0, 0]
        for person in persons_all:
            persons_all_count[person.gender] += 1
        query = '''SELECT DISTINCT app_person.id, app_person.gender, app_person.month_income 
            FROM app_person 
            INNER JOIN app_payment ON (app_person.id=app_payment.person_id) 
            WHERE ''' + income_query
        persons_with_payments = Person.objects.raw(query)
        persons_with_payments_count = [0, 0]
        for person in persons_with_payments:
            persons_with_payments_count[person.gender] += 1
        percent = list(map(lambda a, b: (str(round(100 * b / a)) if a>0 else '0') + '%', persons_all_count, persons_with_payments_count))
        data = []
        if income == need_income:
            if need_all:
                data = persons_all
            else:
                data = persons_with_payments
        result.append({
            'data': data,
            'income': income,
            'all': persons_all_count,
            'with_payments': persons_with_payments_count,
            'percent': percent
        })
    return result
