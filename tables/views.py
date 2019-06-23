from django.shortcuts import render
from plotly.offline import plot
import map.utils as ut
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# import pandas as pd
import app.queries as cu

@login_required(login_url=reverse_lazy('login'))
def table(request):
    data = cu.person_count()

    data2 = []
    for field in data:
        data2.append({
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

    return render(request, 'table.html', {'data': data2})

