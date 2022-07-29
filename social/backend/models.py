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
    created = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=30, null=False)
    phone_number = models.IntegerField(null=False)
    dob = models.IntegerField(null=False)
    username = models.CharField(max_length=30, null=True, unique=True) 
    bio = models.TextField(max_length=160, null=True)
    friend_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True)
        
    objects = CustomAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["full_name", "phone_number", "dob"]

    def __str__(self):
        return str(f"Name: {self.full_name}, Phone Number: {self.phone_number}")


class Login(models.Model):
    phone_number = models.IntegerField(unique=True, null=False)
    code = models.CharField(max_length=6, null=False)
 
    
class ResendOTP(models.Model):
    phone_number = models.IntegerField(unique=True, null=False)