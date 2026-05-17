import logging

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Robot
from .serializers import RobotSerializer


logger = logging.getLogger(__name__)


class RobotListCreateAPIView(APIView):

    def get(self, request):

        robots = Robot.objects.all()

        serializer = RobotSerializer(
            robots,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = RobotSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RobotRetrieveUpdateAPIView(APIView):

    def get(self, request, robot_id):

        try:
            robot = Robot.objects.get(
                robot_id=robot_id
            )

        except Robot.DoesNotExist:
            return Response(
                {"error": "Robot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RobotSerializer(robot)

        return Response(serializer.data)

    def patch(self, request, robot_id):

        try:
            robot = Robot.objects.get(
                robot_id=robot_id
            )

        except Robot.DoesNotExist:
            return Response(
                {"error": "Robot not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RobotSerializer(
            robot,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RobotHealthAPIView(APIView):

    def get(self, request, robot_id):

        heartbeat = cache.get(
            f"robot:{robot_id}:heartbeat"
        )

        if heartbeat:
            return Response({
                "robot_id": robot_id,
                "status": "ONLINE"
            })

        return Response({
            "robot_id": robot_id,
            "status": "OFFLINE"
        })


class RobotStateAPIView(APIView):

    def get(self, request, robot_id):

        state = cache.get(
            f"robot:{robot_id}:state"
        )

        if not state:
            return Response(
                {"error": "State not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(state)