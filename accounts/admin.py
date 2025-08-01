from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.timezone import now
# Register your models here.
from .models import Salary
@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'loan', 'balance', 'get_payment_for')
    readonly_fields = ('balance',)
    list_filter = ('user', 'amount', 'loan')

    def get_payment_for(self, obj):
        return obj.payment_for
    get_payment_for.short_description = 'Payment For'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['full_name','email', 'role', 'is_staff']
    ordering = ['full_name']
    list_filter = ('full_name','email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'address', 'photo', 'next_of_kin', 'next_of_kin_contact')}),
        ('Role and Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )

from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'monthly_repayment', 'total_repayment', 'months_to_repay', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'reason')
    readonly_fields = ('monthly_repayment', 'total_repayment','created_at',)

    fieldsets = (
        ('Loan Details', {
            'fields': ('user', 'amount', 'months_to_repay', 'reason')
        }),
        ('Repayment Info', {
            'fields': ('monthly_repayment', 'total_repayment')
        }),
        ('Approval', {
            'fields': ('status', 'denial_reason')
        }),
    )
