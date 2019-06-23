from django.shortcuts import render
from plotly.offline import plot
import map.utils as ut
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# import pandas as pd
import app.queries as cu

@login_required(login_url=reverse_lazy('login'))
def table(request):
    #Данные о гражданнах, получающих социальные выплаты, по возрастным группам и гендерному признаку
    data_pc = cu.person_count()
    data_vg = []
    for field in data_pc:
        data_vg.append({
            'age': str(field['age']).replace(',', ' - ').replace('[', '').replace(']', ''),
            'woman': {
                'all': field['all'][0],
                'with_payments': field['with_payments'][0],
                'percent': field['percent'][0],
            },
            'men': {
                'all': field['all'][1],
                'with_payments': field['with_payments'][1],
                'percent': field['percent'][1],
            }
        })

    #Данные о гражданнах, получающих социальные выплаты, по возрастным группам и территориальному признаку
    data_gc = cu.gorod_selo()
    data_vt = []
    for field in data_gc:
        all_city = field['all']['work_city'] + field['all']['nowork_city']
        all_village = field['all']['work_village'] + field['all']['nowork_village']
        data_vt.append({
            'age': str(field['age']).replace(',', ' -').replace('[', '').replace(']', ''),
            'city': {
                'all': all_city,
                'work_city': field['with_payments']['work_city'],
                'nowork_city': field['with_payments']['nowork_city']
            },
            'village': {
                'all': all_village,
                'work_village': field['with_payments']['work_village'],
                'nowork_village': field['with_payments']['nowork_village']
            }
        })
    return render(request, 'table.html', {'data_vt': data_vt, 'data_vg': data_vg})

