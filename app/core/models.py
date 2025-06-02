""""
Database models for the core app."""

from django.db import models # noqa

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users."""
    # ** means we can pass any number of keyword arguments to the method
    # This is useful when you define additional fields, for example, a name,
    # you can pass it as an extra field and that will be automatically be created
    # when the user model is created.
    # And it just gives you a bit of flexibility when it comes to creating different
    # fields in the user. It means any time you add new fields here,
    # you don't need to update the create user method. You can just automatically
    # provide them when you're calling the Create User method and it will automatically
    # pass any values you give to the new model
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        # self.model is a reference to the User model clas defined below
        # user = self.model(email=email, **extra_fields)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using self._db allows us to specify which database to use
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
            """Create and return a new superuser."""
            user = self.create_user(email, password)
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)

            return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
