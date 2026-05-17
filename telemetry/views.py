import time
import logging

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from robots.models import Robot

from .models import RobotEvent
from .serializers import RobotEventSerializer


logger = logging.getLogger(__name__)


class TelemetryIngestAPIView(APIView):

    def post(self, request):

        robot_id = request.data.get("robot_id")

        if not robot_id:

            return Response(
                {"error": "robot_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        telemetry = {

            "x": request.data.get("x", 0),

            "y": request.data.get("y", 0),

            "speed": request.data.get("speed", 0),

            "heading": request.data.get(
                "heading",
                "north"
            ),

            "status": request.data.get(
                "status",
                "IDLE"
            ),

            "battery": request.data.get(
                "battery",
                100
            )
        }

        cache.set(
            f"robot:{robot_id}:state",
            telemetry,
            timeout=300
        )

        return Response({
            "message": "Telemetry updated"
        })


class HeartbeatAPIView(APIView):

    def post(self, request):

        robot_id = request.data.get("robot_id")

        if not robot_id:

            return Response(
                {"error": "robot_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache.set(
            f"robot:{robot_id}:heartbeat",
            time.time(),
            timeout=30
        )

        return Response({
            "message": "Heartbeat received"
        })


class LiveTelemetryAPIView(APIView):

    def get(self, request):

        robots = Robot.objects.all()

        response = []

        for robot in robots:

            state = cache.get(
                f"robot:{robot.robot_id}:state"
            )

            if state:

                response.append({

                    "robot_id": robot.robot_id,

                    "state": state
                })

        return Response(response)


class RobotTelemetryAPIView(APIView):

    def get(self, request, robot_id):

        state = cache.get(
            f"robot:{robot_id}:state"
        )

        if not state:

            return Response(
                {"error": "Telemetry not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(state)


class RobotEventsAPIView(APIView):

    def get(self, request, robot_id):

        events = RobotEvent.objects.filter(
            robot__robot_id=robot_id
        ).order_by("-created_at")

        serializer = RobotEventSerializer(
            events,
            many=True
        )

        return Response(serializer.data)