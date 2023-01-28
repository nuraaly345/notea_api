from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManage

class UserManager(BaseUserManage):
    use_in_migrations = True

    def create_user(self, email, name=None, password=None, full_name=None, is_active=None, is_staff=None, is_admin=None  ):
        if not email:
            raise ValueError('Колдонуучуда E-mail адрес болушу зарыл')
        if not password:
            raise ValueError('Колдонуучу паролдуу киргизүүсү керек')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=False)

        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=False)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(null=True, blank=True, max_length=255)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
