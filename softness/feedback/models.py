from django.db import models

from users.models import User


# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_feedbacks",
        on_delete=models.CASCADE
    )
    message = models.CharField(
        max_length=500,
        verbose_name='Текст сообщения от пользователя',
    )

    class Meta:
        verbose_name = "Сообщение от пользователя"
        verbose_name_plural = "Сообщение от пользователя"

    def __str__(self):
        return self.message[:30] + ((lambda message: "..." if len(message) > 30  else "")(self.message))
