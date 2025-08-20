"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import path, re_path
from django.conf import settings

from agentapp.tasks import AskOpenaiConsumer
from agentapp.SSEHttpConsumer import SSEHttpConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": URLRouter([
      path("streaming/", SSEHttpConsumer.as_asgi()),
      re_path(r"^(?!streaming).*", get_asgi_application()),
    ]),
    "channel": ChannelNameRouter({
        "ask_openai_channel": AskOpenaiConsumer.as_asgi(),
    }),
})
