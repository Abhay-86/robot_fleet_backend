from django.urls import path

from .views import (
    MissionListCreateAPIView,
    MissionRetrieveAPIView,
    CancelMissionAPIView,

    MoveForwardAPIView,
    MoveBackwardAPIView,

    TurnLeftAPIView,
    TurnRightAPIView,

    StopRobotAPIView,
    SetSpeedAPIView,

    FleetOverviewAPIView,
    TelemetryUpdateAPIView,
)

urlpatterns = [

    path('missions/',MissionListCreateAPIView.as_view(),name='mission-list-create'),
    path('missions/<str:mission_id>/',MissionRetrieveAPIView.as_view(),name='mission-detail'),
    path('missions/<str:mission_id>/cancel/',CancelMissionAPIView.as_view(),name='cancel-mission'),
    path('robots/<str:robot_id>/forward/',MoveForwardAPIView.as_view(),name='move-forward'),
    path('robots/<str:robot_id>/backward/',MoveBackwardAPIView.as_view(),name='move-backward'),
    path('robots/<str:robot_id>/left/',TurnLeftAPIView.as_view(),name='turn-left'),
    path('robots/<str:robot_id>/right/',TurnRightAPIView.as_view(),name='turn-right'),
    path('robots/<str:robot_id>/stop/',StopRobotAPIView.as_view(),name='stop-robot'),
    path('robots/<str:robot_id>/speed/',SetSpeedAPIView.as_view(),name='set-speed'),
    path('overview/',FleetOverviewAPIView.as_view(),name='fleet-overview'),
    path('telemetry/',TelemetryUpdateAPIView.as_view(),name='telemetry-update'),
]