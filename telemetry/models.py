from django.db import models

from robots.models import Robot


class RobotEvent(models.Model):

    EVENT_CHOICES = [
        ("BATTERY_LOW", "BATTERY_LOW"),
        ("ROBOT_ONLINE", "ROBOT_ONLINE"),
        ("ROBOT_OFFLINE", "ROBOT_OFFLINE"),
        ("MISSION_STARTED", "MISSION_STARTED"),
        ("MISSION_COMPLETED", "MISSION_COMPLETED"),
        ("ERROR", "ERROR"),
    ]

    robot = models.ForeignKey(
        Robot,
        on_delete=models.CASCADE,
        related_name="events"
    )

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )

    payload = models.JSONField(
        default=dict
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.robot.robot_id} - {self.event_type}"