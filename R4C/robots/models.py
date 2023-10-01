from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)


class RobotStatus(models.Model):
    robot = models.OneToOneField(Robot, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=10, default='available')
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Robot)
def create_robot_status(sender, instance, created, **kwargs):
    if created:
        RobotStatus.objects.create(robot=instance)