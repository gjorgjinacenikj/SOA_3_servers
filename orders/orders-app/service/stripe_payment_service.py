import pybreaker
import stripe
from sqlalchemy.orm import Session

from repository.CircuitBreakerListener import CircuitBreakerListener

from web.dtos import PaymentDTO
from repository.crud import get_order_by_id
from repository.repo_models import Order

payment_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=10, listeners=[CircuitBreakerListener()])


def after_pay(db: Session, order: Order):
    order.paid = True
    db.add(order)
    db.commit()
    db.refresh(order)



@payment_breaker
def execute_payment(paymentDto: PaymentDTO, db: Session):
    order = get_order_by_id(db, paymentDto.orderId)
    if paymentDto.paymentMethodId is not None:
        # Create new PaymentIntent with a PaymentMethod ID from the client.

        intent = stripe.PaymentIntent.create(
            amount=int(order.amount_paid * 100),
            currency=paymentDto.currency,
            payment_method=paymentDto.paymentMethodId,
            confirmation_method='manual',
            # If a mobile client passes `useStripeSdk`, set `use_stripe_sdk=true`
            # to take advantage of new authentication features in mobile SDKs.
            use_stripe_sdk=True if 'useStripeSdk' in paymentDto and paymentDto.useStripeSdk else None,
        )

        intent = stripe.PaymentIntent.confirm(
            intent.id,
            payment_method="pm_card_visa"
        )
        after_pay(db, order)
        receipt_url = intent.charges.data[0].receipt_url
        # After create, if the PaymentIntent's status is succeeded, fulfill the order.
    elif paymentDto.paymentIntentId is not None:
        # Confirm the PaymentIntent to finalize payment after handling a required action
        # on the client.
        intent = stripe.PaymentIntent.confirm(paymentDto.paymentIntentId)

        # After confirm, if the PaymentIntent's status is succeeded, fulfill the order.
    return intent
