from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "https://www.example.com"
    client_class = OAuth2Client


class View(RetrieveAPIView):
    def get(self, request: Request, *args, **kwargs):

        print(request.user)

        return Response(data={
            "alo": "bre"
        })
