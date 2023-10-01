from .models import *
from orders.models import Order
from django.core.mail import send_mail


@receiver(post_save, sender=RobotStatus)
def notify_customers(sender, instance, created, **kwargs):
    if created and instance.status == 'available':
        orders = Order.objects.filter(robot_serial=instance.robot.serial)
        if orders.exists():
            for order in orders:
                customer = order.customer
                send_mail(
                    'Робот доступен',
                    f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.robot.model}, версии {instance.robot.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.',
                    'your_email@example.com',  # Замените на вашу электронную почту
                    [customer.email],
                    fail_silently=False,
                )
