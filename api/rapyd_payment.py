from pprint import pprint
from flask import redirect
import time
from utilities import make_request


# Create a payment
"""
def create_payment(total_sum):
    data = {
        "amount": total_sum,
        "currency": "ISK",
        "payment_method": {
            "type": 'is_visa_card',
            "fields": {
                "number": "4111111111111111",
                "expiration_month": "12",
                "expiration_year": "27",
                "cvv": "567",
                "name": "John Doe"
            }
        }
    }
    response = make_request(method='post',
                            path='/v1/payments',
                            body=data)

    amount = data['amount']

    merchant_reference_id = response['data']['merchant_reference_id']

    customer_token = response['data']['customer_token']

    expiration_ts = response['data']['expiration']
"""

# Create a checkout page
def create_checkout_page(amount, merchant_reference_id, expiration_ts=time.time() + 604800):
    
    checkout_page = {
    "amount": amount,
    "complete_payment_url": "https://biryani-ai-pal.vercel.app/successful_payment",
    "country": "IS",
    "currency": "ISK",
    #"customer": customer_token,
    "error_payment_url": "https://biryani-ai-pal.vercel.app/error_payment",
    "merchant_reference_id": merchant_reference_id,
    "language": "en",
    "metadata": {
        "merchant_defined": True
    },
    "expiration": expiration_ts,
    "payment_method_types_include": [
        "is_visa_card",
        "is_mastercard_card"
    ]
}
    result = make_request(method='post', path='/v1/checkout', body=checkout_page)

    checkout_page_url = result['data']['redirect_url']

    return checkout_page_url



checkout_page_url = create_checkout_page(7777, "3333-7777")

print(checkout_page_url)

     


