from django.shortcuts import render


def about(request):
    #assert False
    return render(request, 'about.html')


def project(request):
    #assert False
    return render(request, 'project.html')
