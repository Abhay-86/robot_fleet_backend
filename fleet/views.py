import logging
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

from robots.models import Robot

from .models import Mission
from .serializers import MissionSerializer

from fleet_backend.zenoh_service import (
    send_robot_command
)


logger = logging.getLogger(__name__)


class MissionListCreateAPIView(APIView):

    def get(self, request):

        missions = Mission.objects.all()

        serializer = MissionSerializer(
            missions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        robot_id = request.data.get("robot_id")

        try:
            robot = Robot.objects.get(
                robot_id=robot_id
            )

        except Robot.DoesNotExist:

            return Response(
                {"error": "Robot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        mission = Mission.objects.create(
            mission_id=str(uuid.uuid4()),
            robot=robot,
            start_x=request.data.get("start_x", 0),
            start_y=request.data.get("start_y", 0),
            target_x=request.data.get("target_x", 0),
            target_y=request.data.get("target_y", 0),
        )

        serializer = MissionSerializer(mission)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MissionRetrieveAPIView(APIView):

    def get(self, request, mission_id):

        try:
            mission = Mission.objects.get(
                mission_id=mission_id
            )

        except Mission.DoesNotExist:

            return Response(
                {"error": "Mission not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MissionSerializer(mission)

        return Response(serializer.data)


class CancelMissionAPIView(APIView):

    def post(self, request, mission_id):

        try:
            mission = Mission.objects.get(
                mission_id=mission_id
            )

        except Mission.DoesNotExist:

            return Response(
                {"error": "Mission not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        mission.status = "FAILED"

        mission.save()

        return Response({
            "message": "Mission cancelled"
        })


class MoveForwardAPIView(APIView):

    def post(self, request, robot_id):

        send_robot_command(
            robot_id,
            "w"
        )

        logger.info(f"{robot_id} FORWARD")

        return Response({
            "message": "forward command sent"
        })


class MoveBackwardAPIView(APIView):

    def post(self, request, robot_id):

        send_robot_command(
            robot_id,
            "s"
        )

        logger.info(f"{robot_id} BACKWARD")

        return Response({
            "message": "backward command sent"
        })


class TurnLeftAPIView(APIView):

    def post(self, request, robot_id):

        send_robot_command(
            robot_id,
            "a"
        )

        logger.info(f"{robot_id} LEFT")

        return Response({
            "message": "left command sent"
        })


class TurnRightAPIView(APIView):

    def post(self, request, robot_id):

        send_robot_command(
            robot_id,
            "d"
        )

        logger.info(f"{robot_id} RIGHT")

        return Response({
            "message": "right command sent"
        })


class StopRobotAPIView(APIView):

    def post(self, request, robot_id):

        send_robot_command(
            robot_id,
            "stop"
        )

        logger.info(f"{robot_id} STOP")

        return Response({
            "message": "stop command sent"
        })


class SetSpeedAPIView(APIView):

    def post(self, request, robot_id):

        speed = request.data.get("speed", 0)

        send_robot_command(
            robot_id,
            "set_speed",
            speed
        )

        return Response({
            "robot_id": robot_id,
            "speed": speed
        })


class FleetOverviewAPIView(APIView):

    def get(self, request):

        robots = Robot.objects.all()

        fleet_state = []

        for robot in robots:

            state = cache.get(
                f"robot:{robot.robot_id}:state"
            )

            heartbeat = cache.get(
                f"robot:{robot.robot_id}:heartbeat"
            )

            fleet_state.append({

                "robot_id": robot.robot_id,

                "online": bool(heartbeat),

                "state": state
            })

        return Response({

            "total_robots": robots.count(),

            "active_missions": Mission.objects.filter(
                status="RUNNING"
            ).count(),

            "robots": fleet_state
        })


class TelemetryUpdateAPIView(APIView):
    """
    Receive telemetry data from robots and update cache
    """
    
    def post(self, request):
        robot_id = request.data.get("robot_id")
        state = request.data.get("state")
        
        if not robot_id or not state:
            return Response(
                {"error": "robot_id and state are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update state in cache (expires in 5 seconds)
        cache.set(
            f"robot:{robot_id}:state",
            state,
            timeout=5
        )
        
        # Update heartbeat (expires in 3 seconds)
        cache.set(
            f"robot:{robot_id}:heartbeat",
            True,
            timeout=3
        )
        
        logger.info(
            f"Telemetry updated for {robot_id}: "
            f"x={state.get('x', 0):.1f}, y={state.get('y', 0):.1f}"
        )
        
        return Response({"status": "ok"})