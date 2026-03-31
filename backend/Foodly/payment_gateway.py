import os
import uuid


try:
    import stripe
except ImportError:
    stripe = None


def process_payment(payment_method, amount_kwd, metadata=None):
    metadata = metadata or {}

    if payment_method == 'cash_on_delivery':
        return {
            'status': 'pending',
            'reference': f'cod-{uuid.uuid4().hex[:12]}',
            'provider': 'cash_on_delivery',
        }

    stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')
    if stripe and stripe_secret_key:
        stripe.api_key = stripe_secret_key
        amount_fils = int(round(float(amount_kwd) * 1000))

        intent = stripe.PaymentIntent.create(
            amount=amount_fils,
            currency='kwd',
            payment_method_types=['card'],
            metadata=metadata,
            confirm=False,
        )
        return {
            'status': 'authorized',
            'reference': intent.id,
            'provider': 'stripe',
        }

    return {
        'status': 'authorized',
        'reference': f'mock-{uuid.uuid4().hex[:12]}',
        'provider': 'mock_gateway',
    }
