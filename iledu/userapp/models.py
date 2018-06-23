from django.db import models

# Create your models here.
import hashlib
from django.db import models

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=255, primary_key=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True,default='teammate')
    avatar = models.CharField(max_length=255, null=True, blank=True,default='/static/avatar/default.jpg')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    @property
    def get_id(self):
        return self.nt_id

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name if self.first_name is not None and self.last_name is not None else ""

    @property
    def get_password(self):
        raise AttributeError('password is not a readable attribute')

    @get_password.setter
    def set_password(self, password):
        self.password = hashlib.md5(password).hexdigest()

    def verify_password(self, password):
        self.password = '' if self.password is None else self.password

        return self.password == hashlib.md5(password).hexdigest()

    def __str__(self):
        return self.get_full_name + " ({0})".format(self.get_id)
