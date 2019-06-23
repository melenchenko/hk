from .models import Person, Payment, PaymentType, IncomeType, Family, City
import joblib, os
from django.db import connection


AGES = [
    [0, 18],
    [18, 25],
    [25, 30],
    [30, 40],
    [40, 50],
    [50, 60],
    [60, 80],
    [80, 1000],
]
INCOMES = [
    [0, 0.01],
    [0.01, 10000],
    [10000, 15000],
    [15000, 20000],
    [20000, 30000],
    [30000, 40000],
    [40000, 60000],
    [60000, 100000],
    [100000, 150000],
    [150000, 200000000],
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


def payment_sum():
    """ Выплаты
    [{'name': 'Единовременная выплата по рождению ребенка', 'sum': Decimal('9887695.00')},
    """
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


def get_persons(payments_only = True, need_where = [], need_join = []):
    if payments_only:
        query = '''SELECT DISTINCT p.* FROM app_person p
        INNER JOIN app_payment pay ON (p.id=pay.person_id)'''
    else:
        query = 'SELECT * FROM app_person'
    return Person.objects.raw(query)


def income_type():
    """ ДОоходы """
    persons = get_persons()
    incomes = IncomeType.objects.all()
    sum = 0
    result = {}
    for person in persons:
        sum = sum + person.month_income
    for income in incomes:
        result[income.id] = {'name': income.name, 'sum': 0}
    for person in persons:
        result[person.main_income_type_id]['sum'] += person.month_income
    for income in incomes:
        result[income.id]['percent'] = (str(round(100 * result[income.id]['sum'] / sum)) if sum > 0 else '0') + '%'
    return result


def gorod_selo():
    persons_all_query = '''SELECT DISTINCT p.id, s.type, p.work_status
        FROM app_person p 
        INNER JOIN app_city s ON (s.id=p.city_id)
        WHERE '''
    persons_with_payments_query = '''SELECT DISTINCT p.id, s.type, p.work_status
        FROM app_person p 
        INNER JOIN app_city s ON (s.id=p.city_id)
        INNER JOIN app_payment pay ON (p.id=pay.person_id)
        WHERE '''
    result = []
    for age in AGES:
        age_query = AGE_NUMBER + '>= ' + str(age[0]) + ' AND ' + AGE_NUMBER + '< ' + str(age[1])
        query = persons_all_query + age_query
        persons_all = Person.objects.raw(query)
        all = {
            'work_city': 0,
            'work_village': 0,
            'nowork_city': 0,
            'nowork_village': 0,
        }
        for person in persons_all:
            if (person.type == 1):
                if (person.work_status == 1):
                    all['work_city'] += 1
                else:
                    all['nowork_city'] += 1
            else:
                if (person.work_status == 1):
                    all['work_village'] += 1
                else:
                    all['nowork_village'] += 1
        query = persons_with_payments_query + age_query
        persons_with_payments = Person.objects.raw(query)
        with_payments = {
            'work_city': 0,
            'work_village': 0,
            'nowork_city': 0,
            'nowork_village': 0,
        }
        for person in persons_with_payments:
            if (person.type == 1):
                if (person.work_status == 1):
                    with_payments['work_city'] += 1
                else:
                    with_payments['nowork_city'] += 1
            else:
                if (person.work_status == 1):
                    with_payments['work_village'] += 1
                else:
                    with_payments['nowork_village'] += 1
        result.append({
            'age': age,
            'all': all,
            'with_payments': with_payments,
        })
    return result

#запускать асинхронно каждый раз, когда меняется person[family_id] или добавляется новый person
def child_count_populate():
    query = 'SELECT COUNT(*) as `child_count`, family_id as `id` FROM app_person GROUP BY family_id'
    fam = Family.objects.raw(query)
    for f in fam:
        query = 'UPDATE app_family SET child_count=' + str(f.child_count) + ' WHERE id=' + str(f.id)
        with connection.cursor() as cursor:
            cursor.execute(query)


def family_report():
    filename = 'fits.dumps/family_report.pkl'
    if os.path.exists(filename):
        pre = joblib.load(filename)
    else:
        families = Family.objects.all()
        pre = {'gorod': [0]*7, 'selo': [0]*7}
        for f in families:
            parents = Person.objects.filter(is_child=0, family_id=f.id)
            cnt = 0
            num_parents = 0
            for parent in parents:
                if Payment.objects.filter(person_id = parent.id).count():
                    num_parents += 1
                    if parent.city.type == 1:
                        cnt += 1
                        if cnt == 2:
                            break
            if num_parents > 0:
                if cnt >= 1:
                    pre['gorod'][min(6, f.child_count)] += 1
                else:
                    pre['selo'][min(6, f.child_count)] += 1
        joblib.dump(pre, filename)
    return pre #[0] - количество семей без детей, [1] - с одним ребенком, [6] - 6 и более детей


def big_data_query():
    query = '''SELECT p.*, SUM(pay.payment_sum) AS `_sum`, 
	COUNT(pay.id) AS `_cnt`, 
	f.child_count,
	(SELECT SUM(cost) FROM app_capital WHERE `person_id`=p.id) `_cap_cost`,
	(SELECT COUNT(`id`) FROM app_capital WHERE `person_id`=p.id) `_cap_count`,
	a1.`value` `answer1`, a2.`value` `answer2`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=1 AND `person_id`=p.id GROUP BY `person_id`) `_pt1_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=1 AND `person_id`=p.id GROUP BY `person_id`) `_pt1_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=2 AND `person_id`=p.id GROUP BY `person_id`) `_pt2_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=2 AND `person_id`=p.id GROUP BY `person_id`) `_pt2_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=3 AND `person_id`=p.id GROUP BY `person_id`) `_pt3_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=3 AND `person_id`=p.id GROUP BY `person_id`) `_pt3_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=4 AND `person_id`=p.id GROUP BY `person_id`) `_pt4_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=4 AND `person_id`=p.id GROUP BY `person_id`) `_pt4_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=5 AND `person_id`=p.id GROUP BY `person_id`) `_pt5_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=5 AND `person_id`=p.id GROUP BY `person_id`) `_pt5_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=6 AND `person_id`=p.id GROUP BY `person_id`) `_pt6_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=6 AND `person_id`=p.id GROUP BY `person_id`) `_pt6_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=7 AND `person_id`=p.id GROUP BY `person_id`) `_pt7_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=7 AND `person_id`=p.id GROUP BY `person_id`) `_pt7_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=8 AND `person_id`=p.id GROUP BY `person_id`) `_pt8_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=8 AND `person_id`=p.id GROUP BY `person_id`) `_pt8_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=9 AND `person_id`=p.id GROUP BY `person_id`) `_pt9_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=9 AND `person_id`=p.id GROUP BY `person_id`) `_pt9_cnt`,
	(SELECT SUM(payment_sum) FROM app_payment WHERE `payment_type_id`=10 AND `person_id`=p.id GROUP BY `person_id`) `_pt10_sum`,
	(SELECT COUNT(payment_sum) FROM app_payment WHERE `payment_type_id`=10 AND `person_id`=p.id GROUP BY `person_id`) `_pt10_cnt`,
	f.fpriznak_id `_family_priznak`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=1) `_priz1`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=2) `_priz2`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=3) `_priz3`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=4) `_priz4`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=5) `_priz5`,
	(SELECT IF(COUNT(id)=0,0,1) FROM app_personpriznaklink WHERE `person_id`=p.id AND `priznak_id`=6) `_priz6`
FROM app_payment pay 
RIGHT JOIN app_person p ON (p.id=pay.person_id) 
LEFT JOIN app_family f ON (p.family_id=f.id)
LEFT JOIN app_answers a1 ON (a1.person_id=p.id AND a1.id=1)
LEFT JOIN app_answers a2 ON (a2.person_id=p.id AND a2.id=1)
WHERE pay.payment_date>='2018-01-01' AND pay.payment_date<'2018-02-01'
GROUP BY (p.id)'''
    return Person.objects.raw(query)
