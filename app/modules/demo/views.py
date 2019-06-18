from django.shortcuts import render, redirect
from app.forms import LoadForm
from .models import Demo, DEMO_SCHEMA
from django.contrib.auth.decorators import login_required
from app.data import scatterplot

@login_required
def load(request):
    if request.method == "POST":
        form = LoadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.type = 'Demo'
            post.save()
            return redirect('demo-view', pk=post.pk)
    else:
        form = LoadForm()
    return render(request, 'demo/load.html', {'form': form})

@login_required
def settings(request):
    return render(request, 'demo/settings.html', {})

@login_required
def graph(request, pk):
    data = Demo.objects.filter(load_id=pk)
    data1 = Demo.objects.filter(load_id=pk, iris='Iris-setosa')
    data2 = Demo.objects.filter(load_id=pk, iris='Iris-versicolor')
    data3 = Demo.objects.filter(load_id=pk, iris='Iris-virginica')
    graph = scatterplot({'Iris-setosa': data1, 'Iris-versicolor': data2, 'Iris-virginica': data3}, DEMO_SCHEMA)
    return render(request, 'demo/graph.html', {'graph': graph})

@login_required
def view(request, pk):
    data = Demo.objects.filter(load_id=pk)
    return render(request, 'demo/view.html', {'data': data})

@login_required
def analyze(request):
    return render(request, 'demo/analyze.html', {})
