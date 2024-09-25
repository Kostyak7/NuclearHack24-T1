from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hackathon24.settings')


from Hackathon24.consumers import PrinterConsumer

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/', PrinterConsumer.as_asgi())
        ])
    )
})
