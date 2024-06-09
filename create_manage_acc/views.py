global bankBal

from django.shortcuts import render,redirect
from decimal import Decimal
from create_manage_acc.models import BankAccount
from . import views
from create_manage_acc.forms import AccountRegForm, BankAccountForm
from django.contrib.auth.models import Group
from loans_borrower.models import Loans, Payment
import datetime
from django.db.models.functions import ExtractMonth, ExtractYear
from bank_calculator.views import pmt
import logging
import uuid
from django.shortcuts import get_object_or_404
from django.db import models
from django.db import transaction

# Create your views here.
def account_registration(request):
    user = request.user
    loans = Loans.objects.filter(user=user)
    
    group = Group.objects.get(name='hasbankaccount')
    
    if(request.method == 'POST'):
        form = AccountRegForm()
        form = AccountRegForm(
            {
                'user': request.user,
                'first_name': request.POST.get('first_name'),
                'last_name' : request.POST.get('last_name'),
                'sex': request.POST.get('sex'),
                'marital_status' : request.POST.get('marital_status'),
                'email': request.POST.get('email'),
                'prefix': request.POST.get('prefix'),
                'address': request.POST.get('address'),
                'phone': request.POST.get('phone')
            })
        print(form.errors)
        if form.is_valid():
            bankBal = request.session.get('bankBal')
            if bankBal is None:
                bankBal = 0
            request.session['bankBal'] = bankBal
            user.groups.add(group)
            print("valid form")
            form.save()
            print(bankBal)
            return redirect('/create-manage-account/deposit-money' ,{'bankBal': bankBal})
    form = AccountRegForm()
    return render(request, 'create_manage_acc/create-acc.html', {'form':form})

def generate_deposit_id():
    return uuid.uuid4().hex

def deposit_money(request):
    logger = logging.getLogger(__name__)
    form = BankAccountForm(request.POST or None)
    try:
        bank_acc = BankAccount.objects.filter(user=request.user).latest('id')
        bank_bal = float(bank_acc.balance)
        deposit_amount = float(bank_acc.deposit)
    except BankAccount.DoesNotExist:
        print("No bank account found for the user.")
        bank_bal = 0  # Default balance if no account exists
    print(bank_bal, deposit_amount, bank_bal+deposit_amount)
    if request.method == 'POST':
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.deposit_id = generate_deposit_id()  # Assuming you have a function to generate this
            deposit.status = 'Pending'
            deposit.balance = Decimal(bank_bal)
            deposit.save()
            print(deposit.reference_number, deposit.id, deposit.deposit_id, deposit.balance+deposit.deposit)
            print(f"Deposit saved with ID {deposit.id}")
            return render(request, 'create_manage_acc/confirmation.html', {'deposit': deposit_amount, 'form': form, 'bank_bal': bank_bal})
        else:
            logger.error("Form is not valid")
            logger.error(form.errors)

    return render(request, 'create_manage_acc/deposit-money.html', {'deposit': deposit_amount, 'form': form, 'bank_bal': bank_bal})

def js_redirect(request):
    context = {'redirect_url': 'confirmation/'}
    return render(request, 'create_manage_acc/confirmation.html', context)

def approve_deposit(request, deposit_id):
    with transaction.atomic():
        deposit = BankAccount.objects.select_for_update().get(pk=deposit_id)
        user = deposit.user
        if deposit.status != 'Approved':
            print(f"Current balance before approval: {user} {deposit.balance}")
            print(f"Deposit amount being approved: {deposit.deposit}")
            deposit.status = 'Approved'
            newbal = deposit.balance + deposit.deposit
            deposit.balance = newbal
            deposit.save()
            print(f"New balance after approval: {user} {deposit.balance}")
    deposit.save()
    return redirect('view_deposit_applications')

def reject_deposit(request, deposit_id):
    deposit = get_object_or_404(BankAccount, pk=deposit_id)
    deposit.status = 'Rejected'
    deposit.save()
    return redirect('view_deposit_applications')

def view_deposit_applications(request):
    deposits = BankAccount.objects.filter(status='Pending').order_by('-id')
    print(deposits)  # Debug: Print deposits to check
    return render(request, 'create_manage_acc/deposit_applications.html', {'deposits': deposits})

def confirmation(request):
    return render(request, 'create_manage_acc/confirmation.html')

def my_dues(request):
    user = request.user
    payments = Payment.objects.filter(loan__user=user, loan__status='Approved').annotate(month=ExtractMonth('due_date')).values('month').annotate(total_due=models.Sum('amount_due')).order_by('month')
    return render(request, 'create_manage_acc/my_dues.html', {'payments': payments})

def all_dues(request):
    payments = Payment.objects.filter(loan__status='Approved').select_related('loan__user').order_by('due_date')
    return render(request, 'create_manage_acc/all_dues.html', {'payments': payments})