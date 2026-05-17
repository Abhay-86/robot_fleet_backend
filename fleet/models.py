from django.db import models

from robots.models import Robot


class Mission(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("RUNNING", "RUNNING"),
        ("COMPLETED", "COMPLETED"),
        ("FAILED", "FAILED"),
    ]

    mission_id = models.CharField(
        max_length=100,
        unique=True
    )

    robot = models.ForeignKey(
        Robot,
        on_delete=models.CASCADE,
        related_name="missions"
    )

    start_x = models.FloatField()

    start_y = models.FloatField()

    target_x = models.FloatField()

    target_y = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    started_at = models.DateTimeField(
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.mission_id