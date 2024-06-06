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
    logger.debug("Received POST data: %s", request.POST)
    amount_paid = request.POST.get('deposit')
    if amount_paid is None:
        amount_paid = 0  # Default value if not provided
    else:
        amount_paid = float(amount_paid)
    if not BankAccount.objects.filter(user = request.user).exists():
        print("does not exist")
        form = BankAccountForm()
        if(request.method == 'POST'):
            if request.POST.get('balance') is None:
                
                form = BankAccountForm({
                    'user':request.user,
                    'deposit': request.POST.get('deposit'),
                    'balance': 0
                    })
            if form.is_valid():
                form.save()
                return render(request, 'create_manage_acc/deposit-money.html', {'form':form, })
        return render(request, 'create_manage_acc/deposit-money.html', {'form':form, })        
    bank_acc = BankAccount.objects.filter(user = request.user).latest('id')
    bankBal = bank_acc.balance
    deposit = request.POST.get('deposit')
    if deposit is not None:
        bankBal = float(deposit) + float(bankBal)
    else:
        # Handle the case where deposit is None, perhaps by setting a default value or returning an error message
        bankBal += 0  # Example: default to adding 0 if no deposit is provided
    form = BankAccountForm()

    if(request.method == 'POST'):

        # Generate a unique deposit_id
        deposit_id = generate_deposit_id()

        bankBal = float(request.POST.get('deposit')) + float(bankBal)

        form = BankAccountForm({
            'user':request.user,
            'deposit': request.POST.get('deposit'),
            'balance': bankBal
            })
        if form.is_valid():
            post = form.save(commit=False)
            post.deposit_id = deposit_id  # Assign the generated deposit_id
            post.save()
            return render(request, 'create_manage_acc/deposit-money.html', {'form':form, 'bank_bal': bankBal, 'deposit_id': deposit_id})

    form = BankAccountForm()
    return render(request, 'create_manage_acc/deposit-money.html', {'form':form, 'bank_bal': bankBal})

def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(BankAccount, pk=deposit_id)
    deposit.status = 'Approved'
    deposit.save()
    return redirect('approve_deposit')

def reject_deposit(request, deposit_id):
    deposit = get_object_or_404(BankAccount, pk=deposit_id)
    deposit.status = 'Rejected'
    deposit.save()
    return redirect('reject_deposit')

def submit_deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            new_deposit = form.save(commit=False)
            new_deposit.user = request.user
            new_deposit.save()
            return redirect('view_deposits')  # Redirect to the deposits view page
    else:
        form = DepositForm()
    return render(request, 'submit_deposit.html', {'form': form})

def view_deposits(request):
    deposits = BankAccount.objects.all()  # Or filter based on certain criteria
    return render(request, 'create_manage_acc/view-deposits.html', {'deposits': deposits})
