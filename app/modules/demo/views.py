from django.shortcuts import render, redirect
from app.forms import LoadForm
from app.models import Settings
from app.loaders import payment_saver
from .models import Demo, DEMO_SCHEMA, DEMO_SCHEMA_priz3, PredictForm, SettingsForm, BIGDATA_CONFIG
from django.contrib.auth.decorators import login_required
from app.data import scatterplot, fit, parse_form
from django.urls import reverse_lazy
from app.queries import big_data_query


@login_required(login_url=reverse_lazy('login'))
def load(request):
    if request.method == "POST":
        form = LoadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            module_name = 'Payment'
            post.type = module_name
            post.save()
            Settings.objects.get_or_create(module=module_name, key='load_id', defaults = {'value': post.id})
            success, errors = payment_saver(post)
            if success:
                return redirect('page-main')
            else:
                return render(request, 'errors.html', {'errors': errors})
            # return redirect('demo-view_', pk=post.pk)
    else:
        form = LoadForm()
    return render(request, 'demo/load.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            load_id = form.cleaned_data['load_id']
            Settings.objects.update_or_create(module='Demo', key='load_id', defaults = {'value': load_id.id})
    else:
        current = Settings.objects.get(module='Demo', key='load_id').value
        form = SettingsForm(initial={'load_id': current})
    return render(request, 'demo/settings.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def graph(request, pk=0):
    if pk == 0:
        pk = Settings.objects.get(module='Demo', key='load_id').value
    data1 = Demo.objects.filter(load_id=pk, iris='Iris-setosa')
    data2 = Demo.objects.filter(load_id=pk, iris='Iris-versicolor')
    data3 = Demo.objects.filter(load_id=pk, iris='Iris-virginica')
    graph = scatterplot({'Iris-setosa': data1, 'Iris-versicolor': data2, 'Iris-virginica': data3}, DEMO_SCHEMA)
    return render(request, 'demo/graph.html', {'graph': graph})


@login_required(login_url=reverse_lazy('login'))
def view(request, pk=0):
    if pk == 0:
        pk = Settings.objects.get(module='Demo', key='load_id').value
    data = Demo.objects.filter(load_id=pk)
    return render(request, 'demo/view.html', {'data': data})


@login_required(login_url=reverse_lazy('login'))
def analyze(request, pk=0):
    result = 'Input data to predict'
    if request.method == "POST":
        form = PredictForm(request.POST)
        if form.is_valid():
            if pk == 0:
                pk = Settings.objects.get(module='Demo', key='load_id').value
            data = Demo.objects.filter(load_id=pk)
            predictor = fit(data, DEMO_SCHEMA, pk)
            # result_ = predictor.predict([[4.9, 4, 1, 0.4]])
            prepare_data = parse_form(form, DEMO_SCHEMA)
            result_ = predictor.predict(prepare_data)
            result = result_[0]
    else:
        form = PredictForm()
    return render(request, 'demo/analyze.html', {'result': result, 'form': form})


@login_required(login_url=reverse_lazy('login'))
def analyze_bigdata(request, type):
    result = 'Введите данные для прогнозирования'
    if request.method == "POST":
        form = BIGDATA_CONFIG[type]['form'](request.POST)
        if form.is_valid():
            data = big_data_query()
            predictor = fit(data, BIGDATA_CONFIG[type]['schema'])
            prepare_data = parse_form(form, BIGDATA_CONFIG[type]['schema'])
            result_ = predictor.predict(prepare_data)
            result = result_[0]
    else:
        form = BIGDATA_CONFIG[type]['form']()
    return render(request, 'demo/analyze.html', {'result': result, 'form': form, 'title': BIGDATA_CONFIG[type]['schema']['title']})
