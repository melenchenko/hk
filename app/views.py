from django.shortcuts import render
from app.utils import save_url

def test(request):
    save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    return render(request, 'app.html', {})
