
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imdb/', include('imdb_app.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('account/', include('user_app.api.urls')),
]
