from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$',
            consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/room/module/(?P<module_id>\d+)/$',
            consumers.ModuleChatConsumer.as_asgi()),
    re_path(r'ws/chat/room/user/(?P<user_slug>[^/]+)/$',
            consumers.UserConsumer.as_asgi()),
]
