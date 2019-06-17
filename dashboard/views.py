from django.shortcuts import render
from dashboard.utils import Card, Graph, Histogram
import random
import datetime

# Create your views here.


def dash(request):
    # Вызов бизнес логики для получение данных

    # Верхние карточки
    card1 = Card("Карточка №1", "1000 р", "-10%", [random.randint(1, 10) for _ in range(0, 8)])
    card2 = Card("Карточка №2", "2000 р", "+10%", [random.randint(1, 10) for _ in range(0, 8)])
    card3 = Card("Карточка №3", "3000 р", "-15%", [random.randint(1, 10) for _ in range(0, 8)])
    card4 = Card("Карточка №4", "4000 р", "+15%", [random.randint(1, 10) for _ in range(0, 8)])

    # Маленький график справа
    sm_graph1 = Graph("Показатель №1", "text-primary")
    sm_graph2 = Graph("Показатель №2", "text-secondary")

    # Chart слева
    charts = (Graph("Мужчины", "text-primary", random.randint(1, 10)),
              Graph("Женщины", "text-secondary", random.randint(1, 10)),
              Graph("Дети", "text-info", random.randint(1, 10)))
    chart_data = []
    for chart in charts:
        chart_data.append(f"[{chart.name}, {chart.data}]")

    # Таблица

    table = {'name': 'Большая таблица', 'headers': ('Дата', 'Название', 'Комментарий', 'Статус'),
             'data': (
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                       'Название', 'Случилось что-то хорошее', 'Хорошо', ),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                       'Название', 'Посто информация', 'Инфо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                       'Название', 'Посто информация', 'Предупреждение',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                    'Название', 'Посто информация', 'Плохо', )
             ),
             }
    table['len'] = range(len(table['headers'])-1)

    histogram = Histogram('Гистограмма с накоплением', ('Данные1', 'Данные2', 'Данные3'),
                          [[1, 2, 3], [3, 4, 6], [8, 1, 6]])


    # Представление на графике
    data = {'name': 'Название DASHBOARD', 'title': 'Заглавие',
            'card1': card1.to_dict(), 'card2': card2.to_dict(), 'card3': card3.to_dict(), 'card4': card4.to_dict(),
            'small_graph': {'name': "Маленький график", 'lines': (sm_graph1, sm_graph2)},
            'chart': {'name': "Круговая диаграмма", 'lines': charts, 'data': chart_data},
            'table': table, 'histogram': histogram,
            }
    return render(request, 'dash_board.html', context=data)

