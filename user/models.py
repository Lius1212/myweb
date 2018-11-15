from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatars', default='avatar/default.png')

    def __str__(self):
        return '<Profile: {} for {}>'.format(self.nickname, self.user.username)
