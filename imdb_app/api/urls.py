from django.urls import path, include
from imdb_app.api import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register('stream',views.StreamPlatformAV, basename='stream')


urlpatterns = [
    path('', include(router.urls)),
    path('watchlist/', views.WatchlistAV.as_view(), name='watchlist'),
    path('filterwatchlist/', views.WatchlistGV.as_view()),
    path('watchlist/<int:pk>/', views.WatchdetailAV.as_view(), name='watchdetail'),
    path('reviews/<int:pk>/', views.ReviewDetailAV.as_view(), name='review'),
    path('watchlist/<int:pk>/reviews/', views.WatchlistwiseReviewAV.as_view(), name='watchlistwisereview'),
    path('watchlist/<int:pk>/createreview/', views.WatchlistwiseReviewCreateAV.as_view(), name='review-create'),
]
