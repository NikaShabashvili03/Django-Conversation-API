from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from channels.db import database_sync_to_async

class CustomWebSocketMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
        super().__init__(inner) 

    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))
        cookies = headers.get(b'cookie', b'').decode('utf-8')
        session_token = self.get_cookie_value(cookies, 'sessionId')
        scope['session_token'] = session_token

        if session_token:
            print("true")
            from django.apps import apps
            from main.models import Session

            apps.get_app_config('main') 

            try:
                session = await database_sync_to_async(Session.objects.get)(session_token=session_token)
                user = await database_sync_to_async(lambda: session.user)()

                if session.expires_at > timezone.now():
                    scope['user'] = user 
                else:
                    await database_sync_to_async(session.delete)() 
                    await self.close_connection(send, code=4003, message="Session expired")
                    return
            except Session.DoesNotExist:
                await self.close_connection(send, code=4003, message="Invalid session token")
                return
        else:
            return await self.close_connection(send, code=4003, message="Invalid session token")
        
        return await self.inner(scope, receive, send)
    
    @staticmethod
    async def close_connection(send, code, message):
        """Send a close frame to the WebSocket client."""
        await send({
            "type": "websocket.close",
            "code": code,
            "reason": message,
        })

    @staticmethod
    def get_cookie_value(cookie_header, key):
        """Parse cookies from the cookie header and retrieve a specific key's value."""
        cookies = {}
        for cookie in cookie_header.split(';'):
            name, _, value = cookie.strip().partition('=')
            cookies[name] = value
        return cookies.get(key)