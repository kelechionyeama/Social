from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_user(self, phone_number, full_name, username, dob, password=None ,**otherfields):
        if not phone_number:
            raise ValueError("You must provide a Phone Number")

        user = self.model(phone_number=phone_number, full_name=full_name, username=username, dob=dob)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, full_name, dob, password=None, **otherfields):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            dob=dob,
            username=username,
            password=password
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    #####################
   # Change DOB AND CODE #
    #####################

    # Profile
    full_name = models.CharField(max_length=30, null=False)
    phone_number = models.IntegerField(unique=True, null=False)
    dob = models.IntegerField(null=False)
    username = models.CharField(max_length=30, null=True, unique=True) 
    friend_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True)
        
    objects = CustomAccountManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "full_name", "dob"]

    def __str__(self):
        return str(f"Name: {self.full_name}, Phone Number: {self.phone_number}")


class Login(models.Model):
    phone_number = models.IntegerField(unique=True, null=True)
    code = models.CharField(max_length=6, null=False)
    
