from django.shortcuts import render
from .models import Wallet_User, Wallet_transactions
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages

# Create your views here.


@login_required
def user_wallet(request):
    storage = messages.get_messages(request)
    storage.used = True

    if not Wallet_User.objects.filter(user_id=request.user).exists():
        wallet = Wallet_User.objects.create(user_id=request.user)
    wallet = Wallet_User.objects.get(user_id=request.user)
    wallet_all = Wallet_transactions.objects.filter(wallet_id=wallet).order_by(
        "-date_of_transaction"
    )[:5]
    context = {
        "wallet": wallet,
        "wallet_all": wallet_all,
    }
    return render(request, "user/wallet.html", context)


@login_required
def update_wallet_balance(request):
    if request.method == "POST":
        amount_str = request.POST.get("amount")
        razorpay_payment_id = request.POST.get("payment_id")
        user = request.user
        
        if not amount_str:
            return JsonResponse({"status": "error", "message": "No amount provided."}, status=400)
        
        amount = Decimal(amount_str).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        if not Wallet_User.objects.filter(user_id=user).exists():
            wallet = Wallet_User.objects.create(user_id=user)

        wallet_entry = Wallet_User.objects.get(user_id=user)
        wallet_entry.balance += Decimal(amount)
        wallet_entry.save()

        wallet_history = Wallet_transactions(
            wallet_id=wallet_entry,
            transaction_for="Razor Pay",
            amount_received=Decimal(amount),
        )
        wallet_history.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
