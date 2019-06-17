from django.shortcuts import render

def load(request):
    return render(request, 'demo/load.html', {})

def settings(request):
    return render(request, 'demo/settings.html', {})

def view(request):
    return render(request, 'demo/view.html', {})

def analyze(request):
    return render(request, 'demo/analyze.html', {})