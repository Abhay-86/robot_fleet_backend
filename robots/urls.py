from django.urls import path

from .views import (
    RobotListCreateAPIView,
    RobotRetrieveUpdateAPIView,
    RobotHealthAPIView,
    RobotStateAPIView,
)

urlpatterns = [

    path('',RobotListCreateAPIView.as_view()),
    path('<str:robot_id>/',RobotRetrieveUpdateAPIView.as_view()),
    path('<str:robot_id>/health/',RobotHealthAPIView.as_view()),
    path('<str:robot_id>/state/',RobotStateAPIView.as_view()),
]