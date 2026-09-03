import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .cybersource import get_capture_context, extract_card_last4, process_payment

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def payment_page(request):
    if request.method == "POST":
        transient_token = request.POST.get("transient_token", "")
        request.session["payment_data"] = {
            "student_number":  request.POST.get("student_id", ""),
            "payment_amount":  request.POST.get("amount", ""),
            "email":           request.POST.get("email", ""),
            "cardholder_name": request.POST.get("full_name", ""),
            "card_last4":      extract_card_last4(transient_token),
            "transient_token": transient_token,
        }
        return redirect("payment_confirm")

    try:
        origin          = request.scheme + "://" + request.get_host()
        capture_context = get_capture_context(origin)
    except Exception as e:
        logger.error("Failed to get Cybersource capture context: %s", e)
        capture_context = None

    return render(request, "payments/payment_page.html", {
        "capture_context": capture_context,
    })


@require_http_methods(["GET", "POST"])
def payment_confirm(request):
    data = request.session.get("payment_data")
    if not data:
        return redirect("payment_page")

    if request.method == "POST":
        result = process_payment(
            transient_token = data.get("transient_token", ""),
            amount          = data.get("payment_amount", "0"),
            student_number  = data.get("student_number", ""),
            email           = data.get("email", ""),
            cardholder_name = data.get("cardholder_name", ""),
        )

        if result["success"]:
            request.session.pop("payment_data", None)
            request.session["transaction_id"] = result["transaction_id"]
            return redirect("payment_success")

        return render(request, "payments/payment_confirm.html", {
            "data":  data,
            "error": result.get("error") or "Payment was declined. Please check your card details.",
        })

    return render(request, "payments/payment_confirm.html", {"data": data})


@require_http_methods(["GET"])
def payment_success(request):
    transaction_id = request.session.pop("transaction_id", None)
    return render(request, "payments/payment_success.html", {
        "transaction_id": transaction_id,
    })
