from django.shortcuts import render
from app.utils import save_url, parse_xml
from app.queries import person_count, payment_sum, beneficiary_by_income, income_type, gorod_selo

def test(request):
    # save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    # parse_xml()
    q = gorod_selo()
    return render(request, 'app.html', {})
