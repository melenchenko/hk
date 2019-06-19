from django.shortcuts import render
from plotly.offline import plot
import map.utils as ut
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def table(request):
    #assert False
    big_table = {'name': 'Большая таблица', 'headers': ('Дата', 'Название', 'Комментарий', 'Статус'),
             'data': [
                 ('01.01.2019', 'Телефон', 'Ремонт', 'В работе'),
                 ('02.01.2019', 'Планшет', 'Ремонт', 'В работе'),
                 ('03.01.2019', 'Телефон', 'Гарантийный', 'Ожидает выдачи'),
                 ('04.01.2019', 'Телефон', 'Ремонт', 'Ожидает выдачи'),
                 ('05.01.2019', 'Телефон', 'Гарантийный', 'В работе'),
                 ('06.01.2019', 'Телефон', 'Гарантийный', 'В работе'),
                 ('07.01.2019', 'Телефон', 'В ремонте', 'В работе')
             ]
    }

    return render(request, 'table.html', context=dict(big_table=big_table))
