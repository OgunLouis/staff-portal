
# Create your models here.
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import calendar





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

    full_name = models.TextField(blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='article_images/', blank=True, null=True)
    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_contact = models.CharField(max_length=11, blank=True, null=True)

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