from datetime import datetime, timezone
from datetime import timedelta
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from const import Email
from django.conf import settings


class UserInfo(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='info')
    security_code = models.TextField(default='')
    type = models.IntegerField(default=1)   # 1= General User, 2= Account rep, 3= System Administrative
