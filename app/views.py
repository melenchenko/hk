from django.shortcuts import render
from app.utils import save_url, parse_xml
from app.queries import person_count, payment_sum, beneficiary_by_income, income_type, gorod_selo, child_count_populate, family_report
from .forms import Opros
from .models import Answers, Question, Person, Oprosnik

def main(request):
    # save_url('http://card34.ru/uploads/images/nizkaya-tsena.png')
    # parse_xml()
    # child_count_populate()
    # q = family_report()
    return render(request, 'app.html', {})


def errors(request):
    return render(request, 'app.html', {})


def opros(request, pk):
    if request.method == "POST":
        form = Opros(request.POST, oprosnik_id=pk)
        if form.is_valid():
            oprosnik_ = Oprosnik.objects.get(id=pk)
            questions = Question.objects.filter(oprosnik=oprosnik_)
            for q in questions:
                Answers.objects.update_or_create(
                    defaults = {'value': form.cleaned_data['question_' + str(q.id)]},
                    question = Question.objects.get(id=q.id),
                    person = Person.objects.get(snils=form.cleaned_data['snils'])
                )
        return render(request, 'opros.html', {'form': form})
    else:
        form = Opros(oprosnik_id=pk)
        return render(request, 'opros.html', {'form': form})
