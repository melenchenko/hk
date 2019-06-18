from django.shortcuts import render
from dashboard.utils import Card, Graph, Chart, Histogram
import random
import datetime
import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools
import dashboard.graphics as gr



# Create your views here.


def dash(request):
    # Вызов бизнес логики для получение данных

    # Верхние карточки
    card1, card2, card3, card4 = gr.cards()

    # Маленький график справа
    sm_graph1 = Graph("Показатель №1", "text-primary")
    sm_graph2 = Graph("Показатель №2", "text-secondary")

    # Chart слева
    left_chart = Chart(name='Круговая диаграмма', lines=[['Men', 100], ['Women', 40], ['Child', 30]])

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
                    'Название', 'Посто информация', 'Плохо', ),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Интересная информация', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Тут что-то написано', 'Плохо', ),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Интересная информация', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Тут что-то написано', 'Хорошо',),
             ),
             }
    table['len'] = range(len(table['headers'])-1)

    # Гистограмма слева вверху
    histogram = plot(gr.histogram_top_left(), output_type='div', include_plotlyjs=True)


    # Чарт в центре слева
    plot_chart1 = plot(gr.chart_left_center(), output_type='div', include_plotlyjs=False)

    # Линии в центре справа
    plot_lines1 = plot(gr.lines_right_center(), output_type='div', include_plotlyjs=False)

    # Социальные группы внизу
    social = dict(name='Социальные группы', groups=gr.groups())

    # Регионы внизу
    region = dict(name="Регионы", groups=gr.regions())

    # Представление на графике
    data = {'name': 'Название DASHBOARD', 'title': 'Заглавие',
            'card1': card1.to_dict(), 'card2': card2.to_dict(), 'card3': card3.to_dict(), 'card4': card4.to_dict(),
            'table': table, 'histogram': histogram,
            'plot_chart1': plot_chart1, 'plot_lines1': plot_lines1, 'social': social, 'region': region,
            }
    #assert False
    return render(request, 'dash_board.html', context=data)

