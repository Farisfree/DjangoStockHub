from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False)
    # 其他用户信息字段，例如手机号码、地址等等

    def __str__(self):
        return self.user.username
