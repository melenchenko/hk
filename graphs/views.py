from django.shortcuts import render
from plotly.offline import plot
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from graphs.utils import big_graph
import csv
import scipy as sp


@login_required(login_url=reverse_lazy('login'))
def graph(request):
    b_graph = plot(big_graph(), output_type='div', include_plotlyjs=True)
    #assert False
    return render(request, 'graph.html', context=dict(big_graph=b_graph))

