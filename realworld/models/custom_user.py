from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(blank=True, max_length=100, null=True)
    image = models.CharField(max_length=255, null=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name="follows_by")
    favorite_articles = models.ManyToManyField("Article", related_name="favorites_by")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email

    def following(self, user):
        return self.follows_by.filter(id=user.id).exists()