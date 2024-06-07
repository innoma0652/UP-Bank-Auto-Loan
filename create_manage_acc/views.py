global bankBal

from django.shortcuts import render,redirect
from decimal import Decimal
from create_manage_acc.models import BankAccount
from . import views
from create_manage_acc.forms import AccountRegForm, BankAccountForm
from django.contrib.auth.models import Group
from loans_borrower.models import Loans
import datetime
from django.db.models.functions import ExtractMonth, ExtractYear
from bank_calculator.views import pmt
import logging
import uuid
from django.shortcuts import get_object_or_404

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
        bankBal = float(bank_acc.balance)
        deposit_amount = float(bank_acc.deposit)
    except BankAccount.DoesNotExist:
        logger.error("No bank account found for the user.")
        bankBal = 0  # Default balance if no account exists

    if request.method == 'POST':
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.deposit_id = generate_deposit_id()  # Assuming you have a function to generate this
            deposit.status = 'Pending'
            deposit.save()
            print(deposit.reference_number, deposit.id, deposit.deposit_id)
            logger.info(f"Deposit saved with ID {deposit.id}")
            return render(request, 'create_manage_acc/confirmation.html', {'deposit': deposit_amount, 'form': form, 'bank_bal': bankBal})
        else:
            logger.error("Form is not valid")
            logger.error(form.errors)

    return render(request, 'create_manage_acc/deposit-money.html', {'deposit': deposit_amount, 'form': form, 'bank_bal': bankBal})

def js_redirect(request):
    context = {'redirect_url': 'confirmation/'}
    return render(request, 'create_manage_acc/confirmation.html', context)

def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(BankAccount, pk=deposit_id)
    if deposit.status != 'Approved':
        deposit.status = 'Approved'
        deposit.save()
        user_account = BankAccount.objects.get(user=deposit.user)
        user_account.balance += deposit.amount
        user_account.save()
    return redirect('view_deposit_applications')

def reject_deposit(request, deposit_id):
    deposit = get_object_or_404(BankAccount, pk=deposit_id)
    deposit.status = 'Rejected'
    deposit.save()
    return redirect('view_deposit_applications')

def view_deposit_applications(request):
    deposits = BankAccount.objects.filter(status='Pending')  # Adjust this query as needed
    print(deposits)
    return render(request, 'create_manage_acc/deposit_applications.html', {'deposits': deposits})

def confirmation(request):
    return render(request, 'create_manage_acc/confirmation.html')
