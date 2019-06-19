from django.shortcuts import render
from plotly.offline import plot
import map.utils as ut
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def city_map(request):
    city = plot(ut.town(), output_type='div', include_plotlyjs=True)
    #assert False
    return render(request, 'map-vector.html', context=dict(city=city))
