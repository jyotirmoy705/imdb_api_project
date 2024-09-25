from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class WatchListThrottle(UserRateThrottle):
    scope = "watchlist"
    
class ReviewThrottle(UserRateThrottle):
    scope = "review"