from typing import List

import stripe
from pydantic import BaseModel

class UnsuccessfulResponse(BaseModel):
    error_message: str = "ERROR"


class PaymentDTO(BaseModel):
    paymentIntentId: stripe.PaymentIntent = None
    orderId: int = None
    currency: str = None
    paymentMethodId: str = None
    items: List = None
    useStripeSdk: bool = None
