from django.shortcuts import render, redirect
from app.forms import LoadForm
from .models import Demo
from django.contrib.auth.decorators import login_required

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
def view(request, pk):
    data = Demo.objects.filter(load_id=pk)
    return render(request, 'demo/view.html', {'data': data})

@login_required
def analyze(request):
    return render(request, 'demo/analyze.html', {})
