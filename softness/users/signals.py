from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from cart.models import Cart
from users.models import User


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)