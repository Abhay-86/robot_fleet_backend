from django.db import models

class Robot(models.Model):

    STATUS_CHOICES = [
        ("ONLINE", "ONLINE"),
        ("OFFLINE", "OFFLINE"),
        ("IDLE", "IDLE"),
        ("MOVING", "MOVING"),
        ("ERROR", "ERROR"),
    ]

    robot_id = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    robot_type = models.CharField(
        max_length=50,
        default="AGV"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OFFLINE"
    )

    battery_level = models.FloatField(
        default=100
    )

    firmware_version = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.robot_id