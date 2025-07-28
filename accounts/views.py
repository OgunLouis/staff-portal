from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import StaffSignupForm, StaffUpdateForm
from .models import Salary
from .utils import upload_to_imagekit
from django.conf import settings
from .forms import LoanApplicationForm
from .models import Loan
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import now
from django.template.loader import get_template
from xhtml2pdf import pisa

def home(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = StaffSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid login details'
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    salary = Salary.objects.filter(user=request.user).first()  # Safe fetch
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'salary': salary
    })

@login_required
def edit_profile_view(request):
    print("🔍 Current storage:", settings.DEFAULT_FILE_STORAGE)

    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Upload photo to ImageKit manually
            photo = request.FILES.get('image')
            if photo:
                uploaded_url = upload_to_imagekit(photo)
                if uploaded_url:
                    user.photo = uploaded_url

            user.save()
            return redirect('profile')
    else:
        form = StaffUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def apply_for_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            return redirect('loan_status')  # Create this view later
    else:
        form = LoanApplicationForm()
    return render(request, 'accounts/apply.html', {'form': form})

@login_required
def loan_status(request):
    user_loans = Loan.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(user_loans, 5)  # Show 5 loans per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/status.html', {'loans': page_obj})

@login_required
def generate_payslip(request):
    salary = Salary.objects.get(user=request.user)
    template = get_template('accounts/payslip.html')
    context = {
        'salary': salary,
        'user': request.user,
        'now': timezone.now()
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response