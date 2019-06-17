from django.shortcuts import render, redirect
from .forms import LoadForm
from .models import Load, Demo
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Load)
def demo_saver(sender, **kwargs):
    pass

def load(request):
    if request.method == "POST":
        form = LoadForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.type = 'demo'
            post.save()
            return redirect('demo-view', pk=post.pk)
    else:
        form = LoadForm()
    return render(request, 'demo/load.html', {'form': form})

def settings(request):
    return render(request, 'demo/settings.html', {})

def view(request):
    return render(request, 'demo/view.html', {})

def analyze(request):
    return render(request, 'demo/analyze.html', {})