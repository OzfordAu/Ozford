import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone

import requests
from django.conf import settings

SANDBOX_HOST = "nabgateway-api-test.nab.com.au"
PROD_HOST    = "api.cybersource.com"


def _host():
    return SANDBOX_HOST if getattr(settings, "CYBERSOURCE_SANDBOX", True) else PROD_HOST


def _build_signature_headers(method, path, body_str=""):
    merchant_id   = settings.CYBERSOURCE_MERCHANT_ID
    key_id        = settings.CYBERSOURCE_KEY_ID
    shared_secret = settings.CYBERSOURCE_SHARED_SECRET
    host          = _host()
    method        = method.lower()

    gmt_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    digest   = "SHA-256=" + base64.b64encode(
        hashlib.sha256(body_str.encode("utf-8")).digest()
    ).decode()

    if method in ("post", "put", "patch"):
        header_names = ["host", "date", "(request-target)", "digest", "v-c-merchant-id"]
    else:
        header_names = ["host", "date", "(request-target)", "v-c-merchant-id"]

    value_map = {
        "host":             host,
        "date":             gmt_date,
        "(request-target)": f"{method} {path}",
        "digest":           digest,
        "v-c-merchant-id":  merchant_id,
    }

    sig_string = "\n".join(f"{h}: {value_map[h]}" for h in header_names)
    secret_bytes = base64.b64decode(shared_secret)
    signature    = base64.b64encode(
        hmac.new(secret_bytes, sig_string.encode("utf-8"), hashlib.sha256).digest()
    ).decode()

    sig_header = (
        f'keyId="{key_id}", '
        f'algorithm="HmacSHA256", '
        f'headers="{" ".join(header_names)}", '
        f'signature="{signature}"'
    )

    headers = {
        "Host":            host,
        "Date":            gmt_date,
        "Signature":       sig_header,
        "v-c-merchant-id": merchant_id,
        "Content-Type":    "application/json",
        "Accept":          "application/json",
    }
    if method in ("post", "put", "patch"):
        headers["Digest"] = digest

    return headers


def get_capture_context(origin):
    host     = _host()
    path     = "/microform/v2/sessions"
    body     = {
        "clientVersion": "v2",
        "targetOrigins": [origin],
        "allowedCardNetworks": ["VISA", "MASTERCARD", "AMEX", "JCB"],
        "allowedPaymentTypes": ["PANENTRY"],
    }
    body_str = json.dumps(body, separators=(",", ":"))
    headers  = _build_signature_headers("POST", path, body_str)
    resp     = requests.post(
        f"https://{host}{path}",
        headers=headers,
        data=body_str,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.text


def extract_card_last4(transient_token):
    try:
        payload_b64 = transient_token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        masked  = (
            payload
            .get("content", {})
            .get("paymentInformation", {})
            .get("card", {})
            .get("number", {})
            .get("maskedValue", "")
        )
        return masked[-4:] if masked else "????"
    except Exception:
        return "????"


def process_payment(transient_token, amount, student_number, email, cardholder_name):
    host  = _host()
    path  = "/pts/v2/payments"
    parts = cardholder_name.strip().split() if cardholder_name else [""]
    first = parts[0]
    last  = " ".join(parts[1:]) if len(parts) > 1 else first

    body = {
        "clientReferenceInformation": {
            "code": f"OZFORD-{student_number}-{uuid.uuid4().hex[:8].upper()}"
        },
        "processingInformation": {"capture": True},
        "paymentInformation": {
            "tokenizedCard": {"transientToken": transient_token}
        },
        "orderInformation": {
            "amountDetails": {
                "totalAmount": str(amount),
                "currency":    "AUD",
            },
            "billTo": {
                "firstName":          first,
                "lastName":           last,
                "email":              email,
                "country":            "AU",
                "address1":           "333 Queen St",
                "locality":           "Melbourne",
                "administrativeArea": "VIC",
                "postalCode":         "3000",
            },
        },
        "merchantDefinedInformation": [
            {"key": "1", "value": str(student_number)},
        ],
    }

    body_str = json.dumps(body, separators=(",", ":"))
    headers  = _build_signature_headers("POST", path, body_str)
    resp     = requests.post(
        f"https://{host}{path}",
        headers=headers,
        data=body_str,
        timeout=30,
    )
    result   = resp.json()
    success  = result.get("status") in {"AUTHORIZED", "PENDING", "AUTHORIZED_PENDING_REVIEW"}

    return {
        "success":        success,
        "status":         result.get("status"),
        "transaction_id": result.get("id"),
        "error":          result.get("errorInformation", {}).get("message") if not success else None,
    }
