from django.contrib.auth.backends import ModelBackend, UserModel


class CustomAuthBackend(ModelBackend):

    def authenticate(self, request=None, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = None

        try:
            # try authenticate with username
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:

            try:
                # try authenticate with email
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)
        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user