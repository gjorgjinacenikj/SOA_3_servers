This project contains 3 main services: products, orders, and reviews. 
- The products service contains information about products and does not depend on any of the two other services. 
    - Relevant endpoints:
        - GET /reviews - returns max 100 review
- The orders service enables users to order and pay for products using a credit card. It depends on the product service, from which it gets the price for each product, in order to calculate the total order sum. The payment process is implemented using Stripe and one of the following credit card details can be used for testing:
    - Credit card number: 4242424242424242
    - CVC: any 3 digits
    - Validity date: Any future date
    - Other options can be found on Stripe's testing page documentation: https://stripe.com/docs/testing
- The reviews service enables users to leave a review for a product. This service depends on the orders service, to which it sends a call to check whether the user has previously ordered the product, i.e. to check if they are allowed to write a review for it
    - Relevant endpoints:
        - GET /reviews - returns max 100 reviews
        - GET /reviews?product_id - returns all reviews for a product
        - POST /reviews - creates a new review for the product if the user has previously ordered it
            - Expected request body: {product_id: string, overall: float,
            