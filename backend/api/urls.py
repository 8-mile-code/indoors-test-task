from django.urls import include, path

urlpatterns = [
    path('auth/', include('users.urls')),
    path('cats/', include('cats.urls')),
]
