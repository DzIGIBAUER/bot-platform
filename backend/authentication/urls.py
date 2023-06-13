from django.urls import path, include

from .views import GitHubLogin, View

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path("alo/", View.as_view())
]
