from django.contrib import admin
from .models import *

admin.site.register([
    Load, Person, Payment, Payer, PayerType, PaymentType, Family,
    SpecialAccount, SpecialAccountType, City, Region, Priznak,
    PersonPriznakLink, FamilyPriznak, IncomeType,
    Oprosnik, Question, Answers,
])
