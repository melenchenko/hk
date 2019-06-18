import plotly.graph_objs as go
import random
from dashboard.utils import Card


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

    trace1 = go.Scatter(
        x=[x for x in range(1, 10)],
        y=[random.randint(40, 50) for _ in range(1, 10)],
        mode='lines+markers',
        name="'Доход'",
        hoverinfo='name',
        line=dict(
            shape='linear'
        )
    )

    trace2 = go.Scatter(
        x=[x for x in range(1, 10)],
        y=[random.randint(30, 60) for _ in range(1, 10)],
        mode='lines+markers',
        name="'Расход'",
        hoverinfo='name',
        line=dict(
            shape='linear'
        )
    )

    trace3 = go.Scatter(
        x=[x for x in range(1, 10)],
        y=[random.randint(5, 15) for _ in range(1, 10)],
        mode='lines+markers',
        name="'Остаток'",
        hoverinfo='name',
        line=dict(
            shape='linear'
        )
    )

    data = [trace1, trace2, trace3]
    layout = dict(
        legend=dict(
            y=0.5,
            traceorder='reversed',
            font=dict(
                size=16
            )
        )
    )
    fig = dict(data=data, layout=layout)
    return fig


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