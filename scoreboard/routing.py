from django.urls import re_path

from .consumers import ScoreConsumer

websocket_urlpatterns = [
    re_path(r"ws/score/(?P<score_id>\d+)/$", ScoreConsumer.as_asgi()),
    ]