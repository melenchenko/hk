from django import forms
from .models import Load, Oprosnik, Question


class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = ('title', 'file')


class Opros(forms.Form):
    snils = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        oprosnik_id = kwargs.pop('oprosnik_id', None)
        super(Opros, self).__init__(*args, **kwargs)
        if oprosnik_id:
            oprosnik_ = Oprosnik.objects.get(id=oprosnik_id)
            questions = Question.objects.filter(oprosnik=oprosnik_)
            for q in questions:
                self.fields['question_' + str(q.id)] = forms.IntegerField(min_value=1, max_value=5)
