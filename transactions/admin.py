from transactions.models import Income, Expenditure
from budget.models import Budget, IncomeBudgetItem, ExpenseBudgetItem
from categories.models import IncomeCategory, ExpenditureCategory
from positions.models import Position
from django.contrib import admin

admin.site.register(Income)
admin.site.register(Expenditure)
admin.site.register(IncomeCategory)
admin.site.register(ExpenditureCategory)
admin.site.register(Budget)
admin.site.register(ExpenseBudgetItem)
admin.site.register(Position)
