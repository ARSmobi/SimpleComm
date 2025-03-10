from os import access
from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


# class JWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         query_string = scope.get('query_string', b'').decode()
#         query_params = parse_qs(query_string)
#         token = query_params.get('token', [None])[0]
#
#         if token:
#             try:
#                 access_token = AccessToken(token)
#                 user = await database_sync_to_async(User.objects.get)(id=access_token['user_id'])
#                 scope['user'] = user
#             except Exception as e:
#                 print('Ошибка аутентификации WebSocket: ', e)
#         else:
#             scope['user'] = AnonymousUser()
#
#         return await super.__call__(scope, receive, send)

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user = User.objects.get(id=access_token["user_id"])
                scope["user"] = user
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)