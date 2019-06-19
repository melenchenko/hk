from django.shortcuts import render, redirect
from app.forms import LoadForm
from .models import Demo, DEMO_SCHEMA, PredictForm
from django.contrib.auth.decorators import login_required
from app.data import scatterplot, fit, parse_form

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
def analyze(request, pk):
    result = 'Input data to predict'
    if request.method == "POST":
        form = PredictForm(request.POST)
        if form.is_valid():
            data = Demo.objects.filter(load_id=pk)
            predictor = fit(data, DEMO_SCHEMA)
            # result_ = predictor.predict([[4.9, 4, 1, 0.4]])
            prepare_data = parse_form(form, DEMO_SCHEMA)
            result_ = predictor.predict(prepare_data)
            result = result_[0]
    else:
        form = PredictForm()
    return render(request, 'demo/analyze.html', {'result': result, 'form': form})
