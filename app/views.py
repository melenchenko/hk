from django.shortcuts import render
from app.utils import save_url, parse_xml

def test(request):
    # save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    # parse_xml()
    return render(request, 'app.html', {})
