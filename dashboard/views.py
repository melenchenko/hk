from django.shortcuts import render
import random
import datetime
from plotly.offline import plot
import dashboard.graphics as gr
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def dash(request):
    # Верхние карточки
    card1, card2, card3, card4 = gr.cards()

    # Таблица
    table = {'name': 'Большая таблица', 'headers': ('Дата', 'Название', 'Комментарий', 'Статус'),
             'data': (
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Случилось что-то хорошее', 'Хорошо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Посто информация', 'Инфо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Посто информация', 'Предупреждение',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Посто информация', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Интересная информация', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Тут что-то написано', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Интересная информация', 'Плохо',),
                 ((datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).strftime('%d.%m.%Y'),
                  'Название', 'Тут что-то написано', 'Хорошо',),
             ),
             }
    table['len'] = range(len(table['headers']) - 1)

    # Гистограмма слева вверху
    histogram = plot(gr.histogram_top_left(), output_type='div', include_plotlyjs=True)

    # Чарт в центре слева
    plot_chart1 = plot(gr.chart_left_center(), output_type='div', include_plotlyjs=False)

    # Линии в центре справа
    pl0, pl1 = gr.lines_right_center()
    plot_lines0 = plot(pl0, output_type='div', include_plotlyjs=True)
    plot_lines1 = plot(pl1, output_type='div', include_plotlyjs=False)

    # Чарт Доход
    payment_plt = plot(gr.payment(), output_type='div', include_plotlyjs=True)

    # Город-село
    town, vill = gr.gorod_selo()
    town_plt = plot(town, output_type='div', include_plotlyjs=False)
    vill_plt = plot(vill, output_type='div', include_plotlyjs=False)

    # Социальные группы внизу
    social = dict(name='Социальные группы', groups=gr.groups())

    # Регионы внизу
    region = dict(name="Регионы", groups=gr.regions())
    chart_doh = plot(gr.chart_doh(), output_type='div', include_plotlyjs=True)

    # Доход мужчине-женщины
    bar_dohod = plot(gr.dohg(), output_type='div', include_plotlyjs=False)

    # Представление на графике
    data = {'name': 'Название DASHBOARD', 'title': 'Заглавие',
            'table': table, 'histogram': histogram,
            'plot_chart1': plot_chart1, 'plot_lines1': plot_lines1, 'plot_lines0': plot_lines0,
            'social': social, 'region': region, 'chart_doh': chart_doh, 'chart_payment': payment_plt,
            'town': town_plt, 'vill': vill_plt, 'dohod': bar_dohod
            }
    #assert False
    return render(request, 'dash_board.html', context=data)
