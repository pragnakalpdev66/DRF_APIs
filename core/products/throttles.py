from rest_framework.throttling import UserRateThrottle

class BuyProductThrottle(UserRateThrottle):
    scope = 'buy_product'
