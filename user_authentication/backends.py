from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from user_authentication.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user is None:
                return None
            else:
                valid = user.check_password(password)
                if valid:
                    return user
                else:
                    login_attempt = 0
                    if user.login_attempt is None:
                        login_attempt = 0
                    else:
                        login_attempt = user.login_attempt
                    user.login_attempt = (login_attempt + 1)
                    user.save()
        except User.DoesNotExist:
            return None
