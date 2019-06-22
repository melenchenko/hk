import plotly.graph_objs as go
import random
from dashboard.utils import Card
import app.queries as qu


def chart_left_center():
    """Тут должно быть наполнение какими-то бизнес данными, но пока вот так"""
    fig = {
        "data": [
            {
                "values": [random.randint(1, 10) for _ in range(0, 4)],
                "labels": [
                    "Зарплата",
                    "Пенсия",
                    "Пособия",
                    "Прочее",
                ],
                "domain": {"column": 0},
                "name": "Состав доходов",
                "hoverinfo": "label+percent+name",
                "hole": .4,
                "type": "pie"
            }
        ],
        "layout": {
            "title": "Состав доходов",
            "grid": {"rows": 1, "columns": 1},
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "",
                    "x": 0.20,
                    "y": 0.5
                },
            ]
        }
    }
    return fig


def lines_right_center():

    data = qu.person_count()
    # {'age': [0, 18], 'all': [133, 143], 'with_payments': [117, 116], 'percent': ['88%', '81%']
    x = list()
    total_women = list()
    pay_women = list()
    total_men = list()
    pay_men = list()
    persent_men = list()
    persent_women = list()
    nopay_women = list()
    nopay_men = list()
    for line in data:
        x.append("%s-%s" % (line['age'][0], line['age'][1]))
        total_women.append(line['all'][0])
        total_men.append(line['all'][1])
        pay_women.append(line['with_payments'][0])
        pay_men.append(line['with_payments'][1])
        persent_women.append(line['percent'][0])
        persent_men.append(line['percent'][1])
        nopay_men.append((line['all'][1] - line['with_payments'][1]))
        nopay_women.append(line['all'][0] - line['with_payments'][0])


    trace1 = go.Bar(
        x=x,
        y=nopay_women,
        name="Не получают",
    )

    trace2 = go.Bar(
        x=x,
        y=nopay_men,
        name="Не получают",
    )

    trace3 = go.Bar(
        x=x,
        y=pay_women,
        name="Получают",
    )

    trace4 = go.Bar(
        x=x,
        y=pay_men,
        name="Получают",
    )

    data = [trace2, trace4]
    layout = dict(
        legend=dict(
            traceorder='reversed',
            font=dict(
                size=10
            )
        ),
        showlegend=False,
        barmode='stack',
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig1 = dict(data=data, layout=layout)
    data = [trace1, trace3]
    fig2 = dict(data=data, layout=layout)
    return fig1, fig2


def cards():
    """Заполняет карточки наверху дашборды"""
    card_list = list()
    name = ('Трудоустройство', 'Пособия', 'Доход', 'Здоровье')
    for i in range(0, 4):
        trend = random.randint(-10, 10)
        card_list.append(Card(name=name[i], value=random.randint(2000, 5000), trend=trend, success=(trend >= 0)))
    return card_list


def histogram_top_left():

    name_x = ['2015', '2016', '2017']

    trace1 = go.Bar(
        x=name_x,
        y=[random.randint(20, 60) for _ in range(0, 4)],
        name='Инвалиды'
    )
    trace2 = go.Bar(
        x=name_x,
        y=[random.randint(20, 60) for _ in range(0, 4)],
        name='Малоимущие'
    )

    trace3 = go.Bar(
        x=name_x,
        y=[random.randint(20, 60) for _ in range(0, 4)],
        name='Беременные'
    )

    trace4 = go.Bar(
        x=name_x,
        y=[random.randint(20, 60) for _ in range(0, 4)],
        name='Постадавшие'
    )

    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        barmode='stack'
    )

    return go.Figure(data=data, layout=layout)


def groups():
    """Заполняет социальные группы"""
    group_list = list()
    name = ('Безработные', 'Малоимущие', 'Постадавшие от природных бедствий', 'Постадавшие от техногенных катастроф',
            'Сироты', 'Оставшиеся без попечения родителей')
    for i in range(0, 6):
        trend = random.randint(-10, 10)
        group_list.append(Card(name=name[i], value=random.randint(2000, 5000), trend=trend, success=(trend <= 0)).to_dict())
    return group_list


def regions():
    """Заполняет регионы дашборды"""
    group_list = list()
    name = ('Москва', 'Тула', 'Рязань', 'Тверь',
            'Ростов на Дону', 'Тюмень')
    for i in range(0, 6):
        trend = random.randint(-10, 10)
        group_list.append(Card(name=name[i], value=random.randint(20000, 50000), trend=trend, success=(trend >= 0)).to_dict())
    return group_list