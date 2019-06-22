from django.shortcuts import render
from app.utils import save_url, parse_xml
from app.queries import person_count, payment_sum, beneficiary_by_income, income_type, gorod_selo, child_count_populate, family_report

def main(request):
    # save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    # parse_xml()
    # child_count_populate()
    # q = family_report()
    return render(request, 'app.html', {})

def errors(request):
    return render(request, 'app.html', {})
