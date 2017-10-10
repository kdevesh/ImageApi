''' Management command for generating API key or Token'''
import os
import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token


class PasswordError(Exception):
    ''' Password Exception Class for throwing password mismatch error. '''
    def __init__(self, message):
        super().__init__(message)


class Command(BaseCommand):
    ''' For generating unique token for every user '''
    help = 'Create user and obtain access key'

    def handle(self, *args, **options):
        username = input("Enter username : ")
        password = getpass.getpass("Enter password : ")
        try:
            user = User.objects.get(username=username)
            password_check = user.check_password(raw_password=password)                  # Checking whether entered password matches or not.
            if password_check is False:
                raise PasswordError("You have entered a wrong password.Please try again")
            print("User "+username+" already exists.")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)        # If user does'nt exist then create one and generate Token
            user.save()
            print("User "+username+" created.")
        except PasswordError as exception:                                               # Catching Password mismatch error
            print(exception)
            return
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, username)):                  # Check if media/username folder exists if not exists then create
            pass
        else:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, username))
        token, created = Token.objects.get_or_create(user=user)
        print("Access key for " + username + " : ")
        print(token)
