import stripe
from django.conf import settings
from django.shortcuts import redirect

from borrowings.models import Borrowing, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_total_amount(borrowing: Borrowing) -> int:
    using_days = (borrowing.expected_return_date - borrowing.borrow_date).days
    daily_fee_cents = borrowing.book.daily_fee * 100
    return int(daily_fee_cents) * using_days


def retrieve_existing_unit_amount(borrowing: Borrowing):
    looking_price = calculate_total_amount(borrowing)
    for price in stripe.Price.list():
        if price["unit_amount"] == looking_price:
            return price

    return stripe.Price.create(
        product='prod_PuIXD7rHUrikDl',
        unit_amount=looking_price,
        currency="usd",
    )


def stripe_helper(borrowing):
    price = retrieve_existing_unit_amount(borrowing)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=("http://localhost:8000/api/"
                     "payments/success/"),
        cancel_url="http://localhost:8000/api/payments/cancel/"
    )
    Payment.objects.create(
        borrowing=borrowing,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=price["unit_amount"] / 100,
    )
    return redirect(checkout_session.url, code=303)
