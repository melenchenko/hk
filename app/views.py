from django.shortcuts import render
from app.utils import save_url, parse_xml
from app.queries import person_count, payment_sum, beneficiary_by_income

def test(request):
    # save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    # parse_xml()
    q = person_count()
    return render(request, 'app.html', {})
