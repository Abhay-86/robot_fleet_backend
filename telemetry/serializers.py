from rest_framework import serializers

from .models import RobotEvent


class RobotEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = RobotEvent
        fields = "__all__"