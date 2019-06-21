import requests
import os
import wget
import xmltodict
from datetime import datetime


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
