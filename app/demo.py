from django.shortcuts import render, redirect
from .forms import LoadForm
from .models import Load, Demo
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv

@receiver(post_save, sender=Load)
def demo_saver(sender, instance, **kwargs):
    with open(instance.file.name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            Demo.objects.create(
                load=instance,
                iris=row[4],
                sepal_length=row[0],
                sepal_width=row[1],
                petal_length=row[2],
                petal_width=row[3]
            )

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

def settings(request):
    return render(request, 'demo/settings.html', {})

def view(request, pk):
    data = Demo.objects.filter(load_id=pk)
    return render(request, 'demo/view.html', {'data': data})

def analyze(request):
    return render(request, 'demo/analyze.html', {})
