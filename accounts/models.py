
# Create your models here.
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta 



# Custom manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None  # 👈 Important to disable the default username field

    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number=models.CharField(max_length=11, blank=True,null=True,default="", verbose_name="Staff Phone Contact")
    email = models.EmailField(_('email address'), unique=True)
    address = models.CharField(max_length=150, blank=True, null=True,verbose_name="Home Address")
    photo = models.ImageField(upload_to='article_images/', blank=True, null=True,verbose_name="Staff Image")
    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_contact = models.CharField(max_length=11, blank=True, null=True,verbose_name="Next of Kin Contact Number")
    next_of_kin_address = models.CharField(max_length=100, blank=True, null=True)
    ROLE_CHOICES = [
        ('Operator', 'Operator'),
        ('Finisher', 'Finisher'),
        ('Admin', 'Admin'),
        ('Management', 'Management'),
        ('Accountant', 'Accountant'),
        ('Graphics', 'Graphics'),
        ('Security', 'Security'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Salary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_for = models.CharField(max_length=50, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Automatically calculate balance
        if self.amount is not None and self.loan is not None:
            self.balance = self.amount - self.loan
        else:
            self.balance = 0.00

        # Automatically set payment_for to current month
        current_month = calendar.month_name[now().month]
        self.payment_for = f"Salary for {current_month}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - ₦{self.amount} ({self.payment_for})"
    

from datetime import timedelta
from dateutil.relativedelta import relativedelta  # Make sure python-dateutil is installed

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    months_to_repay = models.PositiveSmallIntegerField()
    interest_rate = models.FloatField(default=0.05)
    total_repayment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    denial_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    repayment_end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        total_with_interest = self.amount + (self.amount * self.interest_rate)
        self.total_repayment = round(total_with_interest, 2)
        self.monthly_repayment = round(self.total_repayment / self.months_to_repay, 2)

        if self.created_at:
            # Use `created_at` to calculate repayment_end_date
            self.repayment_end_date = (self.created_at + relativedelta(months=self.months_to_repay)).date()
        else:
            self.repayment_end_date = (now() + relativedelta(months=self.months_to_repay)).date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan: {self.user.email} - ₦{self.amount} ({self.status})"
