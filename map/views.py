from django.shortcuts import render
import random
import datetime
from plotly.offline import plot
import map.utils as ut


def city_map(request):
    city = plot(ut.town(), output_type='div', include_plotlyjs=True)
    #assert False
    return render(request, 'map-vector.html', context=dict(city=city))
