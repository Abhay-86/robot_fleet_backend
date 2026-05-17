from django.urls import path

from .views import (
    TelemetryIngestAPIView,
    HeartbeatAPIView,
    LiveTelemetryAPIView,
    RobotTelemetryAPIView,
    RobotEventsAPIView,
)

urlpatterns = [

    path('ingest/',TelemetryIngestAPIView.as_view(),name='telemetry-ingest'),
    path('heartbeat/',HeartbeatAPIView.as_view(),name='heartbeat'),
    path('live/',LiveTelemetryAPIView.as_view(),name='live-telemetry'),
    path('<str:robot_id>/',RobotTelemetryAPIView.as_view(),name='robot-telemetry'),
    path('<str:robot_id>/events/',RobotEventsAPIView.as_view(),name='robot-events'),
]