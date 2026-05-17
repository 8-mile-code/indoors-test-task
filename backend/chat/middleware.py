from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_user_by_token(token: str):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        User = get_user_model()
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist, KeyError):
        return AnonymousUser()


class JWTAuthMiddleware:
    """Authenticate WebSocket connections
    using a JWT access token query parameter.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)

        token_list = query_params.get('token')

        if token_list:
            scope['user'] = await get_user_by_token(token_list[0])
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
