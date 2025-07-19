from django.contrib import admin

# Register your models here.
from .models import Salary

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'loan', 'balance', 'payment_for')
    readonly_fields = ('balance', 'payment_for')