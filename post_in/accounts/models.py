from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name=None, password=None, full_name=None, is_active=True, is_staff=None, is_admin=None  ):
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
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=True)

        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password, is_staff=True, is_admin=False)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(null=True, blank=True, max_length=255)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name

        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True

        return self.staff

    @property
    def is_admin(self):
        return self.admin


    def save(self, *args, **kwargs):
        if not self.id and not self.staff and not self.admin:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


