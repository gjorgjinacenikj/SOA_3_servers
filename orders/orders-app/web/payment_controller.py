import stripe
from fastapi import APIRouter, Header, Depends
from requests import Session

from creds import stripe_api_key, stripe_api_key_publishable
from .dtos import PaymentDTO
from repository.database import get_db
from service.stripe_payment_service import execute_payment

#load_dotenv(find_dotenv())
stripe.api_key = stripe_api_key

stripe_router = APIRouter()

@stripe_router.get('/stripe-key', summary="Gets the public stripe api key")
def fetch_key():
    # Send publishable key to client
    return {'publishableKey': stripe_api_key_publishable}


@stripe_router.post('/pay', summary="Executes the payment")
def pay(paymentDto: PaymentDTO, db: Session = Depends(get_db)):

    try:

        intent = execute_payment(paymentDto, db=db)
        response = generate_response(intent)
        return response
    except stripe.error.CardError as e:
        print('error')
        return {'error': e.user_message}


def generate_response(intent):
    status = intent['status']
    print(status)
    if status == 'requires_action' or status == 'requires_source_action':
        # Card requires authentication
        return {'requiresAction': True, 'paymentIntentId': intent['id'], 'clientSecret': intent['client_secret']}
    elif status == 'requires_payment_method' or status == 'requires_source':
        # Card was not properly authenticated, suggest a new payment method
        return {'error': 'Your card was denied, please provide a new payment method'}
    elif status == 'succeeded':
        # Payment is complete, authentication not required
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
        print("💰 Payment received!")
        return {'clientSecret': intent['client_secret']}
