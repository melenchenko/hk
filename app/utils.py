import requests
import os
import wget
import xmltodict
from datetime import datetime
from app.models import City, Region, Person, Payer, PaymentType, Payment
import random
import datetime
from scipy.stats import truncnorm
import random as random_number


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm.cnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')


def save_url(url, path_to_save='uploads/tmp/'):
    # url = 'https://api.github.com/some/endpoint'
    # payload = {'some': 'data'}
    # r = requests.post(url, json=payload)
    # r.text or r.content
    filename = wget.download(url)
    full_path = u'' + os.getcwd() + '/' + path_to_save + filename
    if os.path.exists(full_path):
        os.remove(full_path)
    os.rename(filename, full_path)
    # (dirname, filename) = os.path.split(url)
    # f = open(path_to_save + filename, 'wb')
    # f.write(content)
    # f.close()

def parse_xml(text=''):
    text = """\
<Response>
    <Data>
        <Report>
            <LeaderList>
                <Leader ActualDate="2009-12-01" FIO="Шxxxxxxx Аxxxxx Шxxxxxx" INN="5xxxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2008-10-07" FIO="Вxxxxxx Аxxxxxx Аxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2007-04-17" FIO="Оxxxxxxxx Сxxxxx Вxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2004-12-06" FIO="Кxxxxxxx Аxxxxxxx Нxxxxxx" Position="генеральный директор"/>
            </LeaderList>
        </Report>
    </Data>
    <ResultInfo ExecutionTime="140" ResultType="True"/>
</Response>
"""
    doc = xmltodict.parse(text)
    items = doc['Response']['Data']['Report']['LeaderList']['Leader']

    # Находим максимальный элемент через дату
    leader = max(items, key=lambda x: to_date(x['@ActualDate']))
    print(leader['@FIO'])  # Шxxxxxxx Аxxxxx Шxxxxxx
    print(leader['@ActualDate'])  # 2009-12-01
    print(leader['@Position'])  # генеральный директор


def add_city():
    """Добавить области в БД. Запустить только один раз!"""
    raions = ('Алексинский район', 'Арсеньевский район', 'Белёвский район', 'Богородицкий район', 'Венёвский район',
              'Воловский район', 'Дубенский район', 'Ефремовский район', 'Заокский район',
              'Каменский район', 'Кимовский район', 'Киреевский район', 'Куркинский район',
              'Ленинский район', 'Новомосковский район', 'Одоевский район', 'Плавский район', 'Суворовский район',
              'Тёпло-Огарёвский район', 'Узловский район', 'Чернский район', 'Щёкинский район',
              'Ясногорский район')
    region = Region()
    region.name = 'Тульская область'
    region.save()
    for raion in raions:
        city = City()
        city.region = region
        city.name = raion
        city.save()

def snils(init=0):
    """ Функция генерирует СНИСЛ, начинающийся с 002 (чтобы легче было искать) остальные
    числа случайные, контрольное число вычисляется
    Страховой номер индивидуального лицевого счета страхового свидетельства обязательного пенсионного страхования(он же СНИЛС) проверяется на валидность контрольным числом. СНИЛС имеет вид: «XXX-XXX-XXX YY», где XXX-XXX-XXX — собственно номер, а YY — контрольное число. Алгоритм формирования контрольного числа СНИЛС таков:
    1) Проверка контрольного числа Страхового номера проводится только для номеров больше номера 001-001-998
    2) Контрольное число СНИЛС рассчитывается следующим образом:
    2.1) Каждая цифра СНИЛС умножается на номер своей позиции (позиции отсчитываются с конца)
    2.2) Полученные произведения суммируются
    2.3) Если сумма меньше 100, то контрольное число равно самой сумме
    2.4) Если сумма равна 100 или 101, то контрольное число равно 00
    2.5) Если сумма больше 101, то сумма делится по остатку на 101 и контрольное число определяется остатком от деления аналогично пунктам 2.3 и 2.4
    ПРИМЕР: Указан СНИЛС 112-233-445 95
    Проверяем правильность контрольного числа:
    цифры номера        1 1 2 2 3 3 4 4 5
    номер позиции       9 8 7 6 5 4 3 2 1
    Сумма = 1×9 + 1×8 + 2×7 + 2×6 + 3×5 + 3×4 + 4×3 + 4×2 + 5×1 = 95
    95 ÷ 101 = 0, остаток 95.
    Контрольное число 95 — указано верно """
    if init !=0:
        random.seed(init)
    # заполняем начальные числа СНИСЛ
    arr = [0, 0, 2]
    # res - переменная для результата
    res = ""
    contr = 0
    for i in range(3, 9):
        arr.append(random.randint(0, 9))
    for i in range(0, 9):
        contr += arr[i] * (9 - i)
        res += str(arr[i])
    if contr > 99:
        if contr == 100 or contr == 101:
            contr = 0
        else:
            contr %= 101
    if contr < 10:
        res += "0" + str(contr)
    else:
        res += str(contr)
    return res



def add_people():
    for i in range(0, 1000):
        sex = random.choice((0, 1))
        pers = Person()
        cites = City.objects.all()

        if sex:
            # Мужчина
            name = random.choice(('Иван', 'Федор', 'Никита', 'Николай', 'Сергей', 'Ярослав'))
            famil = random.choice(('Сергеев', 'Степанов', 'Кац', 'Иванов', 'Петров', 'Башаров'))
            otch = random.choice(('Иванович', 'Сергеевич', 'Петрович', 'Дмитриевич', 'Никитович', 'Степанович'))
        else:
            # Женщина
            name = random.choice(('Нина', 'Ирина', 'Соня', 'Виктория', 'Светлана', 'Наталья'))
            famil = random.choice(('Сергеевна', 'Степановна', 'Кац', 'Иванова', 'Петрова', 'Башарова'))
            otch = random.choice(('Ивановна', 'Сергеевна', 'Петровна', 'Дмитриевна', 'Никитовна', 'Степановна'))
        pers.fullname = "%s %s %s" % (name, famil, otch)
        pers.snils = snils()
        pers.city = random.choice(cites)
        h = random_number.normalvariate(2, 2)
        if h < 0:
            h = 0
        elif h > 3:
            h = 3
        pers.health_status = h
        pers.birthday = datetime.datetime.now() - datetime.timedelta(days=random_number.normalvariate(45, 40) * 365)
        income = random_number.normalvariate(3000, 1000)
        if income < 0:
            income = 0
        pers.month_income = income
        pers.gender = sex
        pers.save()


def add_payment():
    persons = Person.objects.all()
    payments =PaymentType.objects.all()
    payers = Payer.objects.all()
    for person in persons:
        # С вероятностью 10% он ничего не получает
        if random.randint(0, 10) >= 9:
            continue
        # А тут получает
        for i in range(random.randint(10, 30)):
            pay = Payment()
            pay.person = person
            pay.payment_sum = random.randint(500, 10000)
            pay.payer = random.choice(payers)
            pay.payment_type = random.choice(payments)
            pay.payment_date = datetime.datetime(year=random.choice((2015, 2016, 2017, 2018)), month=random.randint(1, 12), day=random.randint(1, 27))
            pay.save()




