from django.urls import path
from products.consumers import AdminNotificationConsumer

websocket_urlpatterns = [
    path("ws/admin/notifications/", AdminNotificationConsumer.as_asgi()),
]


# string = "longgg stringgg"
# string2 = sorted(string)
# print(string2)
# print(string2.index("g"))

# print(string2.index('g'))