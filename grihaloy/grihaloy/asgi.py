import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# 1. Set the settings module environment variable FIRST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grihaloy.settings")

# 2. Call get_asgi_application() SECOND. This is what loads your Django settings.
django_asgi_app = get_asgi_application()

# 3. NOW it is safe to import your routing, which imports consumers/models
from properties import routing # NEW

application = ProtocolTypeRouter(
    {
        # 4. Use the Django app you already initialized
        "http": django_asgi_app,

        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(routing.websocket_urlpatterns)
            )
        ),
    }
)